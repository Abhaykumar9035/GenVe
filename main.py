import argparse
import ast
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from gtts import gTTS

from config import config
from manim_gen.manim_generation import ManimCodeGenerator
from modules.scene_management import SceneManager
from modules.script_generation import PreambleGenerator, ScriptGeneration
from modules.topic_refinement import TopicRefinement

DEBUG_LOG_PATH = Path("debug-4a10a2.log")
DEBUG_SESSION_ID = "4a10a2"


def debug_log(hypothesis_id: str, location: str, message: str, data: dict | None = None, run_id: str = "pre-fix") -> None:
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    try:
        with DEBUG_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass


def load_moviepy_clips():
    # region agent log
    debug_log(
        "H1",
        "main.py:39",
        "Inspecting moviepy import specs",
        {
            "moviepy_spec_found": importlib.util.find_spec("moviepy") is not None,
            "moviepy_editor_spec_found": importlib.util.find_spec("moviepy.editor") is not None,
            "python_executable": sys.executable,
        },
    )
    # endregion
    try:
        from moviepy.editor import AudioFileClip, VideoFileClip
        # region agent log
        debug_log("H2", "main.py:52", "Imported from moviepy.editor successfully")
        # endregion
        return AudioFileClip, VideoFileClip
    except Exception as exc:
        # region agent log
        debug_log(
            "H2",
            "main.py:57",
            "moviepy.editor import failed",
            {"error_type": type(exc).__name__, "error": str(exc)},
        )
        # endregion
        try:
            from moviepy import AudioFileClip, VideoFileClip
            # region agent log
            debug_log("H3", "main.py:67", "Imported from moviepy root namespace successfully")
            # endregion
            return AudioFileClip, VideoFileClip
        except Exception as fallback_exc:
            # region agent log
            debug_log(
                "H3",
                "main.py:74",
                "moviepy root import also failed",
                {"error_type": type(fallback_exc).__name__, "error": str(fallback_exc)},
            )
            # endregion
            raise


def ensure_dirs(*dirs: Path) -> None:
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def clean_manim_code(raw_code: str) -> str:
    code = raw_code.strip()
    if code.startswith("```"):
        code = re.sub(r"^```[a-zA-Z]*\n?", "", code, count=1)
        code = re.sub(r"\n?```$", "", code, count=1)
    return code.strip()


def normalize_manim_symbols(manim_code: str) -> str:
    replacements = {
        "WriteText(": "Write(",
    }
    normalized = manim_code
    applied = []
    for old, new in replacements.items():
        if old in normalized:
            normalized = normalized.replace(old, new)
            applied.append({"from": old, "to": new})
    # region agent log
    debug_log(
        "H5",
        "main.py:111",
        "Applied Manim symbol normalization",
        {"replacements": applied, "replacement_count": len(applied)},
        run_id="post-fix",
    )
    # endregion
    return normalized


def normalize_manim_kwargs(manim_code: str) -> str:
    get_size_pattern = r",\s*get_size\s*=\s*[^,\)]*"
    matches = re.findall(get_size_pattern, manim_code)
    normalized = re.sub(get_size_pattern, "", manim_code)
    # region agent log
    debug_log(
        "H7",
        "main.py:128",
        "Applied Manim kwargs normalization",
        {"removed_get_size_count": len(matches)},
        run_id="post-fix",
    )
    # endregion
    return normalized


def normalize_manim_api_calls(manim_code: str) -> str:
    transpose_pattern = r"(\w+)\.transpose\(\)"
    transpose_matches = re.findall(transpose_pattern, manim_code)
    normalized = re.sub(transpose_pattern, r"\1.copy()", manim_code)

    play_mobject_pattern = r"self\.play\((\s*[A-Za-z_]\w*\s*)\)"
    play_mobject_matches = re.findall(play_mobject_pattern, normalized)
    normalized = re.sub(play_mobject_pattern, r"self.play(Write(\1))", normalized)

    play_tail_mobject_count = 0
    rewritten_lines = []
    for line in normalized.splitlines():
        updated_line = line
        if "self.play(" in line and "Write(" not in line:
            tail_match = re.search(r",\s*([A-Za-z_]\w*)\s*\)\s*$", line)
            if tail_match:
                token = tail_match.group(1)
                updated_line = re.sub(r",\s*([A-Za-z_]\w*)\s*\)\s*$", rf", Write({token}))", line)
                play_tail_mobject_count += 1
        rewritten_lines.append(updated_line)
    normalized = "\n".join(rewritten_lines)

    fadeout_all_pattern = r"FadeOut\(all\(\)\)"
    fadeout_all_matches = re.findall(fadeout_all_pattern, normalized)
    normalized = re.sub(fadeout_all_pattern, "FadeOut(*self.mobjects)", normalized)

    end_call_pattern = r"\n\s*self\.end\(\)\s*"
    end_call_matches = re.findall(end_call_pattern, normalized)
    normalized = re.sub(end_call_pattern, "\n", normalized)

    # region agent log
    debug_log(
        "H8",
        "main.py:145",
        "Applied Manim API normalization",
        {
            "replaced_transpose_count": len(transpose_matches),
            "wrapped_play_single_mobject_count": len(play_mobject_matches),
            "wrapped_play_tail_mobject_count": play_tail_mobject_count,
            "replaced_fadeout_all_count": len(fadeout_all_matches),
            "removed_end_call_count": len(end_call_matches),
        },
        run_id="post-fix",
    )
    # endregion
    return normalized


def normalize_latex_unicode(manim_code: str) -> str:
    sigma_count = manim_code.count("σ")
    normalized = manim_code.replace("σ", r"\sigma")
    # region agent log
    debug_log(
        "H9",
        "main.py:176",
        "Applied LaTeX unicode normalization",
        {"sigma_replaced_count": sigma_count},
        run_id="post-fix",
    )
    # endregion
    return normalized


def normalize_matrix_entry_access(manim_code: str) -> str:
    entry_pattern = r"\.move_to\((\w+)\[\d+\s*,\s*\d+\]\)"
    matches = re.findall(entry_pattern, manim_code)
    normalized = re.sub(entry_pattern, r".move_to(\1)", manim_code)
    # region agent log
    debug_log(
        "H10",
        "main.py:193",
        "Applied matrix entry access normalization",
        {"move_to_entry_replaced_count": len(matches)},
        run_id="post-fix",
    )
    # endregion
    return normalized


def detect_scene_class_name(manim_code: str) -> str:
    tree = ast.parse(manim_code)
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "Scene":
                return node.name
            if isinstance(base, ast.Attribute) and base.attr == "Scene":
                return node.name
    raise ValueError("No class inheriting from Scene was found in generated Manim code.")


def extract_narration(script: str) -> str:
    pattern = (
        r"Naration Script:\s*(.*?)"
        r"(?:\n\s*Final Script fot Video Explainer using Narration Script and Visual Cues:|\Z)"
    )
    match = re.search(pattern, script, flags=re.DOTALL)
    if not match:
        raise ValueError("Could not extract 'Naration Script' section from generated script.")
    return match.group(1).strip()


def unwrap_scenes(scene_prediction) -> list:
    scenes_field = scene_prediction.scenes
    return scenes_field.scenes if hasattr(scenes_field, "scenes") else scenes_field


def manim_quality_flag(quality_value: str) -> str:
    mapping = {
        "low_quality": "l",
        "medium_quality": "m",
        "high_quality": "h",
        "production_quality": "p",
        "fourk_quality": "k",
    }
    return mapping.get(quality_value, "m")


def render_manim(scene_file: Path, scene_class: str, media_dir: Path, quality_flag: str) -> Path:
    command = [
        sys.executable,
        "-m",
        "manim",
        f"-q{quality_flag}",
        str(scene_file),
        scene_class,
        "--media_dir",
        str(media_dir),
        "-o",
        "draft",
    ]
    subprocess.run(command, check=True)

    candidates = list(media_dir.rglob("draft.mp4"))
    if candidates:
        return max(candidates, key=lambda p: p.stat().st_mtime)

    all_mp4 = list(media_dir.rglob("*.mp4"))
    if not all_mp4:
        raise FileNotFoundError("Manim render completed but no MP4 output was found.")
    return max(all_mp4, key=lambda p: p.stat().st_mtime)


def generate_audio(narration_text: str, audio_path: Path, language: str = "en") -> Path:
    tts = gTTS(text=narration_text, lang=language)
    tts.save(str(audio_path))
    return audio_path


def mux_video_audio(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    AudioFileClip, VideoFileClip = load_moviepy_clips()
    with VideoFileClip(str(video_path)) as video_clip:
        with AudioFileClip(str(audio_path)) as audio_clip:
            # region agent log
            debug_log(
                "H11",
                "main.py:288",
                "Inspecting audio clip trimming methods",
                {
                    "has_subclip": hasattr(audio_clip, "subclip"),
                    "has_subclipped": hasattr(audio_clip, "subclipped"),
                    "audio_duration": audio_clip.duration,
                    "video_duration": video_clip.duration,
                },
                run_id="post-fix",
            )
            # endregion
            if audio_clip.duration > video_clip.duration:
                if hasattr(audio_clip, "subclip"):
                    final_audio = audio_clip.subclip(0, video_clip.duration)
                elif hasattr(audio_clip, "subclipped"):
                    final_audio = audio_clip.subclipped(0, video_clip.duration)
                else:
                    final_audio = audio_clip
            else:
                final_audio = audio_clip
            # region agent log
            debug_log(
                "H12",
                "main.py:314",
                "Inspecting video audio attach methods",
                {"has_set_audio": hasattr(video_clip, "set_audio"), "has_with_audio": hasattr(video_clip, "with_audio")},
                run_id="post-fix",
            )
            # endregion
            if hasattr(video_clip, "set_audio"):
                final_video = video_clip.set_audio(final_audio)
            elif hasattr(video_clip, "with_audio"):
                final_video = video_clip.with_audio(final_audio)
            else:
                final_video = video_clip
            final_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=video_clip.fps or 24)
    return output_path


def run_pipeline(topic: str, output_path: Path | None = None, quality: str | None = None) -> Path:
    pipeline_cfg = config.get("pipeline", {})
    generated_dir = Path(pipeline_cfg.get("generated_dir", "generated"))
    output_dir = Path(pipeline_cfg.get("output_dir", "output"))
    media_dir = generated_dir / "media"
    ensure_dirs(generated_dir, output_dir, media_dir)

    output_file = output_path or (output_dir / "final.mp4")
    scene_file = generated_dir / "scene.py"
    script_file = generated_dir / "script.txt"
    narration_file = generated_dir / "narration.txt"
    audio_file = generated_dir / "narration.mp3"

    print("[1/7] Refining topic...")
    topic_refiner = TopicRefinement()
    refined = topic_refiner(topic)
    refined_prompt = refined.refined_prompt

    print("[2/7] Generating script...")
    preamble = PreambleGenerator()
    script_generator = ScriptGeneration(preamble)
    script_prediction = script_generator(topic, refined_prompt)
    full_script = script_prediction.final_script
    script_file.write_text(full_script, encoding="utf-8")

    print("[3/7] Breaking script into scenes...")
    scene_manager = SceneManager()
    scene_prediction = scene_manager(full_script)
    scenes = unwrap_scenes(scene_prediction)

    print("[4/7] Generating Manim code...")
    manim_generator = ManimCodeGenerator()
    manim_prediction = manim_generator(scenes)
    manim_code = clean_manim_code(manim_prediction.manim_code)
    # region agent log
    debug_log(
        "H6",
        "main.py:232",
        "Generated Manim code before normalization",
        {"has_write_text": "WriteText(" in manim_code, "code_preview": manim_code[:120]},
    )
    # endregion
    manim_code = normalize_manim_symbols(manim_code)
    manim_code = normalize_manim_kwargs(manim_code)
    manim_code = normalize_manim_api_calls(manim_code)
    manim_code = normalize_latex_unicode(manim_code)
    manim_code = normalize_matrix_entry_access(manim_code)
    # region agent log
    debug_log(
        "H6",
        "main.py:241",
        "Manim code after normalization",
        {
            "has_write_text": "WriteText(" in manim_code,
            "has_write": "Write(" in manim_code,
            "has_get_size_kwarg": "get_size=" in manim_code,
            "has_transpose_call": ".transpose()" in manim_code,
            "has_unicode_sigma": "σ" in manim_code,
        },
        run_id="post-fix",
    )
    # endregion
    scene_file.write_text(manim_code, encoding="utf-8")

    scene_class = detect_scene_class_name(manim_code)
    selected_quality = quality or manim_quality_flag(config["manim_settings"].get("quality", "medium_quality"))

    print("[5/7] Rendering video with Manim...")
    rendered_video = render_manim(scene_file=scene_file, scene_class=scene_class, media_dir=media_dir, quality_flag=selected_quality)

    print("[6/7] Generating narration audio...")
    narration_text = extract_narration(full_script)
    narration_file.write_text(narration_text, encoding="utf-8")
    tts_cfg = pipeline_cfg.get("tts", {})
    generate_audio(narration_text, audio_file, language=tts_cfg.get("language", "en"))

    print("[7/7] Muxing final MP4...")
    mux_video_audio(rendered_video, audio_file, output_file)
    print(f"Done. Final video: {output_file.resolve()}")
    return output_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and render a Manim explainer video with narration.")
    parser.add_argument("--topic", required=True, help="Topic to generate the explainer video for.")
    parser.add_argument(
        "--quality",
        choices=["l", "m", "h", "p", "k"],
        default=None,
        help="Override Manim quality flag (l/m/h/p/k).",
    )
    parser.add_argument("--output", default=None, help="Output MP4 path. Defaults to output/final.mp4.")
    return parser.parse_args()


if __name__ == "__main__":
    # region agent log
    debug_log(
        "H4",
        "main.py:247",
        "Pipeline entrypoint reached",
        {"python_executable": sys.executable, "python_version": sys.version.split()[0]},
    )
    # endregion
    args = parse_args()
    output_arg = Path(args.output) if args.output else None
    run_pipeline(topic=args.topic, output_path=output_arg, quality=args.quality)
