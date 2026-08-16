"""Dependency-free SVG affine transform parsing and composition."""

from __future__ import annotations

import math
import re


Affine = tuple[float, float, float, float, float, float]
IDENTITY: Affine = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
TRANSFORM_RE = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")


def multiply(left: Affine, right: Affine) -> Affine:
    """Compose matrices so ``left`` is applied after ``right``."""
    a, b, c, d, e, f = left
    g, h, i, j, k, l = right
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * l + e,
        b * k + d * l + f,
    )


def parse(value: str) -> Affine:
    result = IDENTITY
    for function, argument_text in TRANSFORM_RE.findall(value):
        arguments = [float(number) for number in re.split(r"[\s,]+", argument_text.strip()) if number]
        if function == "matrix" and len(arguments) == 6:
            operation: Affine = tuple(arguments)  # type: ignore[assignment]
        elif function == "translate" and len(arguments) in {1, 2}:
            operation = (1.0, 0.0, 0.0, 1.0, arguments[0], arguments[1] if len(arguments) == 2 else 0.0)
        elif function == "scale" and len(arguments) in {1, 2}:
            operation = (arguments[0], 0.0, 0.0, arguments[-1], 0.0, 0.0)
        elif function == "rotate" and len(arguments) in {1, 3}:
            radians = math.radians(arguments[0])
            rotation: Affine = (math.cos(radians), math.sin(radians), -math.sin(radians), math.cos(radians), 0.0, 0.0)
            if len(arguments) == 3:
                cx, cy = arguments[1:]
                operation = multiply(
                    (1.0, 0.0, 0.0, 1.0, cx, cy),
                    multiply(rotation, (1.0, 0.0, 0.0, 1.0, -cx, -cy)),
                )
            else:
                operation = rotation
        elif function == "skewX" and len(arguments) == 1:
            operation = (1.0, 0.0, math.tan(math.radians(arguments[0])), 1.0, 0.0, 0.0)
        else:
            raise ValueError(f"unsupported SVG transform: {function}({argument_text})")
        result = multiply(result, operation)
    return result


def text(matrix: Affine) -> str:
    return "matrix(" + " ".join(f"{number:.12g}" for number in matrix) + ")"
