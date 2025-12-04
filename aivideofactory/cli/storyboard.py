++ aivideofactory/cli/storyboard.py
import argparse
import json
import sys
from pathlib import Path

from ..storyboard import StoryboardGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate storyboard JSON using DeepSeek")
    parser.add_argument("--prompt", required=True, help="User prompt that describes the video idea")
    parser.add_argument("--scenes", type=int, help="Number of scenes to request from the model")
    parser.add_argument("--language", default="中文", help="Language for the generated storyboard")
    parser.add_argument("--run-dir", type=Path, help="Optional explicit output directory")
    parser.add_argument("--print", action="store_true", dest="print_json", help="Print the generated JSON to stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    generator = StoryboardGenerator()
    storyboard = generator.run(prompt=args.prompt, scene_count=args.scenes, language=args.language)
    output_path = generator.save(storyboard=storyboard, run_dir=args.run_dir)
    if args.print_json:
        json.dump(storyboard.to_serializable(), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    print(f"Storyboard saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






