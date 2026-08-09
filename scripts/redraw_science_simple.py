#!/usr/bin/env python3
"""Simplify the highest-density science PUA studies into traceable concepts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "science"
INK = 'fill="none" stroke="#262522" stroke-linecap="round" stroke-linejoin="round"'

ART = {
    "fossil": """
<path d="M14 45c-2-12 4-24 16-30 12-2 24 3 29 14 4 10 0 23-10 29-12 5-28 1-35-13z" stroke-width="2.2" {i}/>
<path d="M36 20c9 0 15 7 15 16 0 10-6 16-15 16-8 0-13-6-13-14 0-7 5-12 11-12 6 0 9 4 9 9 0 4-2 7-6 7-3 0-5-2-5-5" stroke-width="1.9" {i}/>
<path d="M18 51c5 3 10 5 16 5M47 18c4 2 7 5 9 9" stroke-width="1.0" opacity=".7" {i}/>
""",
    "chaos": """
<path d="M10 38c8-18 20-23 28-14 7 8-1 18-10 15-9-3-8-14 3-20M62 34c-8 18-20 23-28 14-7-8 1-18 10-15 9 3 8 14-3 20" stroke-width="2.25" {i}/>
<path d="M15 17l5 5M57 17l-5 5M15 55l5-5M57 55l-5-5" stroke-width="1.35" {i}/>
""",
    "honesty": """
<path d="M10 36c7-10 16-15 26-15s19 5 26 15c-7 10-16 15-26 15S17 46 10 36z" stroke-width="2.25" {i}/>
<circle cx="36" cy="36" r="7" stroke-width="1.65" {i}/>
<path d="M15 27c4-5 9-8 15-9M57 27c-4-5-9-8-15-9" stroke-width="1.1" {i}/>
""",
    "galaxy": """
<path d="M36 14c13 0 22 7 21 16-1 10-15 18-27 17-11-1-16-8-11-14 4-5 12-7 18-4 7 3 7 9 2 12-4 3-9 2-11-1" stroke-width="2.35" {i}/>
<path d="M12 19l1 3M58 49l1 3M48 13l1 3M18 52l1 2" stroke-width="1.2" {i}/>
""",
    "climate": """
<path d="M36 12v15M25 17l11 10 11-10M17 43c8-8 15-8 22 0 6 6 12 6 19 0" stroke-width="1.65" {i}/>
<path d="M10 51c9-4 18-4 27 0 8 4 16 4 25 0M13 59c9-3 17-3 25 0 8 3 15 3 21 0" stroke-width="1.35" {i}/>
<path d="M36 29c-4 5-5 8-5 11 0 4 3 7 6 7s6-3 6-7c0-3-2-6-7-11z" stroke-width="1.35" {i}/>
""",
    "evidence": """
<circle cx="31" cy="32" r="16" stroke-width="2.25" {i}/>
<path d="M43 44l16 16M24 37c4-8 9-12 16-15M24 38c4 3 9 3 14 0" stroke-width="2.1" {i}/>
<path d="M16 56c4-3 8-3 12 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "extinction": """
<path d="M12 53c8-8 17-11 27-9 9 2 16 2 22-5" stroke-width="2.0" {i}/>
<path d="M37 44V22M37 28l-8-7M37 34l9-7M37 39l-7-5" stroke-width="1.8" {i}/>
<path d="M18 57c10-2 21-2 37 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "frontier": """
<path d="M8 53l17-20 9 11 13-23 17 32" stroke-width="2.25" {i}/>
<path d="M8 58c16-4 37-4 57 0M13 47c8 1 16 1 25-1" stroke-width="1.25" {i}/>
<path d="M48 21l4-4 4 4" stroke-width="1.15" {i}/>
""",
    "awe": """
<circle cx="36" cy="26" r="5" stroke-width="1.75" {i}/>
<path d="M36 32v18M36 37l-10-8M36 37l10-8M36 50l-7 10M36 50l7 10" stroke-width="2.0" {i}/>
<path d="M12 17l2 4M24 9l1 5M58 9l-1 5M62 17l-2 4" stroke-width="1.25" {i}/>
<path d="M20 62c10-3 22-3 32 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "cosmos": """
<circle cx="36" cy="36" r="15" stroke-width="1.8" {i}/>
<path d="M18 36c7-10 20-15 32-10 8 4 8 12 2 16-6 4-15 2-18-3-3-5 2-9 7-8" stroke-width="2.0" {i}/>
<path d="M12 18l1 4M58 17l-1 4M12 54l2-2M60 53l-2-2" stroke-width="1.15" {i}/>
""",
    "freeze": """
<path d="M36 12v48M16 24l40 24M16 48l40-24M23 16l13 20 13-20M23 56l13-20 13 20" stroke-width="1.75" {i}/>
<path d="M36 12l-3 5M36 12l3 5M16 24l6 1M16 24l3 5M16 48l6-1M16 48l3-5M56 24l-6 1M56 24l-3 5M56 48l-6-1M56 48l-3-5" stroke-width="1.05" {i}/>
""",
    "mentor": """
<circle cx="25" cy="24" r="5" stroke-width="1.75" {i}/><circle cx="47" cy="30" r="5" stroke-width="1.75" {i}/>
<path d="M16 53c1-10 6-16 13-16s11 6 12 16M39 55c1-8 5-13 11-13 5 0 8 4 9 11" stroke-width="2.0" {i}/>
<path d="M31 25c5-4 9-4 14 0M34 20l5-5 5 5" stroke-width="1.35" {i}/>
""",
    "legend": """
<path d="M14 20c10-5 21-5 32 0l12-5v34l-12 5c-11-5-22-5-32 0z" stroke-width="2.1" {i}/>
<path d="M46 20v34M26 26c5-2 10-2 15 0M25 34c5-2 10-2 15 0" stroke-width="1.25" {i}/>
<path d="M20 47l4-5 4 5 5-2" stroke-width="1.1" {i}/>
""",
    "flow": """
<path d="M9 28c8-9 17-9 24 0 7 9 15 9 29-1M9 43c8-9 17-9 24 0 7 9 15 9 29-1M17 57c7-5 14-5 21 0" stroke-width="2.15" {i}/>
<path d="M48 18c4-3 8-3 13 0" stroke-width="1.15" {i}/>
""",
    "contradiction": """
<path d="M21 54c-5-8-3-16 3-22 4-4 5-10 3-16 8 6 10 13 6 20-3 6-2 12 3 18" stroke-width="2.15" {i}/>
<path d="M49 15v38M34 23l30 18M34 41l30-18M40 18l9 18 9-18M40 48l9-18 9 18" stroke-width="1.35" {i}/>
""",
    "cause": """
<path d="M36 13c-5 5-7 9-7 13 0 5 3 8 7 8s7-3 7-8c0-4-2-8-7-13z" stroke-width="1.8" {i}/>
<path d="M36 36c-10 4-16 9-16 15M36 36c10 4 16 9 16 15M12 56c8-3 16-3 24 0 8-3 16-3 24 0" stroke-width="1.55" {i}/>
""",
    "divide": """
<path d="M36 12v48" stroke-width="2.0" {i}/>
<path d="M10 23c8 4 16 4 24 0M10 49c8-4 16-4 24 0M62 23c-8 4-16 4-24 0M62 49c-8-4-16-4-24 0" stroke-width="1.4" {i}/>
<path d="M13 59c7-2 14-2 21 0M59 59c-7-2-14-2-21 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "mist": """
<path d="M10 33c7-7 14-7 21 0 6-7 14-7 21 0 5-4 10-4 14 0M10 45c8-4 16-4 24 0 8-4 16-4 28 0M16 56c7-3 14-3 21 0 7-3 14-3 20 0" stroke-width="1.65" {i}/>
""",
    "history": """
<circle cx="30" cy="35" r="18" stroke-width="2.1" {i}/>
<path d="M30 22v14l8 6M14 21l-5 5M9 26h7" stroke-width="1.55" {i}/>
<path d="M47 47c6 2 9 6 10 11M54 52l4 1-1 4" stroke-width="1.35" {i}/>
""",
    "knowledge": """
<path d="M12 22c8-3 16-2 24 4 8-6 16-7 24-4v35c-8-3-16-2-24 4-8-6-16-7-24-4z" stroke-width="2.1" {i}/>
<path d="M36 26v35M19 31c5-2 10-1 15 2M53 31c-5-2-10-1-15 2" stroke-width="1.25" {i}/>
<path d="M54 15l1 4M50 18l4 1M58 18l-3 1" stroke-width="1.15" {i}/>
""",
    "future": """
<path d="M36 59V33M36 42c-7-8-13-9-19-6 2 8 8 12 19 11M36 38c7-8 13-9 19-6-2 8-8 12-19 11" stroke-width="2.0" {i}/>
<path d="M10 59c9-3 18-3 26 0 8-3 17-3 26 0" stroke-width="1.15" {i}/>
<path d="M36 19l1 4M31 22l5-3 5 3" stroke-width="1.1" {i}/>
""",
    "fraction": """
<circle cx="36" cy="36" r="22" stroke-width="2.1" {i}/>
<path d="M36 14v44M14 36h44" stroke-width="1.45" {i}/>
<path d="M22 22l5 5M50 22l-5 5M22 50l5-5M50 50l-5-5" stroke-width="1.05" {i}/>
""",
    "because": """
<circle cx="22" cy="35" r="10" stroke-width="1.9" {i}/><circle cx="50" cy="35" r="10" stroke-width="1.9" {i}/>
<path d="M32 35h16M22 31l4 4-4 4M50 31l-4 4 4 4" stroke-width="1.35" {i}/>
<path d="M15 18c5-3 10-3 15 0M42 18c5-3 10-3 15 0" stroke-width="1.0" opacity=".7" {i}/>
""",
    "hypothesis": """
<path d="M20 55V25c0-6 6-10 16-10s16 4 16 10v30c-10 4-22 4-32 0z" stroke-width="2.0" {i}/>
<path d="M20 25c10 4 22 4 32 0M29 36c2-5 9-7 12-3 4 5-2 7-5 10-2 2-2 4-2 6M35 52v1" stroke-width="1.45" {i}/>
""",
    "idea": """
<path d="M36 16c-10 0-17 8-17 17 0 6 3 10 7 14v7h20v-7c4-4 7-8 7-14 0-9-7-17-17-17z" stroke-width="2.1" {i}/>
<path d="M30 54h12M31 59h10M36 10v-4M20 12l-3-3M52 12l3-3M14 28H9M58 28h5" stroke-width="1.3" {i}/>
""",
    "explanation": """
<path d="M12 20h48v31H33L22 59v-8H12z" stroke-width="2.05" {i}/>
<path d="M23 30h26M23 38h20M23 46h12" stroke-width="1.25" {i}/>
<path d="M51 13l3 4 5-1-3 4 2 4-5-2-3 3 1-5-4-3 5-1z" stroke-width="1.15" {i}/>
""",
    "exploration": """
<circle cx="30" cy="31" r="16" stroke-width="2.0" {i}/>
<path d="M30 18l4 13-10 8 4-13zM46 47c6 3 9 7 10 12M56 59c-5-1-10 0-15 3" stroke-width="1.5" {i}/>
<path d="M30 12v-4M14 31h-4M30 50v4M46 31h4" stroke-width="1.1" {i}/>
""",
    "art": """
<path d="M14 52c3-11 10-21 19-29 7-6 14-5 18 0 4 6-1 13-8 18-9 7-19 10-29 11z" stroke-width="2.0" {i}/>
<path d="M19 45l11 7M25 37l12 8M33 29l10 7" stroke-width="1.15" {i}/>
<circle cx="54" cy="20" r="3" stroke-width="1.15" {i}/>
""",
    "courage": """
<path d="M36 58V32M36 38l-10-8M36 38l10-8M36 51l-7 9M36 51l7 9" stroke-width="2.0" {i}/>
<circle cx="36" cy="25" r="6" stroke-width="1.8" {i}/>
<path d="M10 28c7-5 13-5 19 0M53 28c4-3 8-3 10 0M9 47c8-4 15-4 22 0M48 47c6-3 11-3 16 0" stroke-width="1.35" {i}/>
""",
    "fall": """
<path d="M36 13c-5 7-7 13-4 17 3 4 9 3 11-2 2-4-1-9-7-15z" stroke-width="1.8" {i}/>
<path d="M38 29c-5 8-9 14-13 19M31 43l-6 5M31 43l1 7" stroke-width="1.45" {i}/>
<path d="M11 58c9-3 18-3 26 0 8-3 17-3 25 0" stroke-width="1.15" {i}/>
""",
    "path": """
<path d="M12 56c8-8 16-14 18-22 2-7-2-12-8-15M60 56c-8-8-16-14-18-22-2-7 2-12 8-15" stroke-width="2.15" {i}/>
<path d="M18 56c10-3 26-3 36 0M24 45c7-2 17-2 24 0M30 34c4-1 8-1 12 0" stroke-width="1.25" {i}/>
<path d="M12 60c16-2 32-2 48 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "evaporation": """
<path d="M10 53c9-4 18-4 27 0 8 4 16 4 25 0" stroke-width="1.7" {i}/>
<path d="M22 43c-4-6 4-8 0-14-3-5 4-7 1-13M36 43c-4-6 4-8 0-14-3-5 4-7 1-13M50 43c-4-6 4-8 0-14-3-5 4-7 1-13" stroke-width="1.85" {i}/>
<path d="M13 59c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "craft": """
<path d="M16 52c5-9 11-16 20-21 7-4 14-3 18 2-5 7-11 13-20 17-7 3-12 4-18 2z" stroke-width="2.1" {i}/>
<path d="M22 47l20-13M28 51l20-13" stroke-width="1.25" {i}/>
<path d="M52 19l1 4M48 21l4 1M56 21l-3 1" stroke-width="1.1" {i}/>
""",
    "exercise": """
<circle cx="36" cy="20" r="5" stroke-width="1.7" {i}/>
<path d="M36 26v18M36 31l-13-7M36 31l13-7M36 44l-8 15M36 44l8 15" stroke-width="2.0" {i}/>
<path d="M17 22h9M46 22h9M20 19v6M52 19v6" stroke-width="1.5" {i}/>
<path d="M15 62c12-3 28-3 42 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "migration": """
<path d="M10 25c5-5 10-5 15 0-5-1-9 0-13 4M27 38c5-5 10-5 15 0-5-1-9 0-13 4M44 25c5-5 10-5 16 0-5-1-10 0-14 4M52 43c4-4 8-4 12 0-4-1-7 0-10 3" stroke-width="2.15" {i}/>
<path d="M8 57c17-3 36-3 57 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "guide": """
<circle cx="28" cy="22" r="5" stroke-width="1.75" {i}/>
<path d="M28 28v24M28 34l-10 8M28 34l10 8M28 52l-7 9M28 52l7 9M48 18v43M44 22h8" stroke-width="1.9" {i}/>
<path d="M9 62c14-3 28-3 52 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "mind": """
<path d="M36 12c-13 0-22 9-22 21 0 11 8 19 18 21v7h8v-7c10-2 18-10 18-21 0-12-9-21-22-21z" stroke-width="2.1" {i}/>
<path d="M36 24c8 0 12 5 9 10-2 4-9 3-11 7-2 4 2 7 7 6" stroke-width="1.55" {i}/>
""",
    "horizon": """
<path d="M9 48c10-8 19-8 27 0 8-8 17-8 27 0M10 57c16-3 34-3 52 0" stroke-width="1.7" {i}/>
<circle cx="36" cy="25" r="9" stroke-width="1.65" {i}/>
<path d="M36 10v5M21 16l4 4M51 16l-4 4" stroke-width="1.15" {i}/>
""",
    "journey": """
<path d="M10 58c10-12 18-15 25-9 7 6 6 10 14 5 5-3 9-8 13-14" stroke-width="2.0" {i}/>
<path d="M14 48c7-4 14-5 20-3M45 38c6-2 11-2 16 0" stroke-width="1.2" {i}/>
<circle cx="22" cy="23" r="4" stroke-width="1.5" {i}/>
<path d="M22 27v13M22 31l-7 5M22 31l7 5M22 40l-5 7M22 40l5 7" stroke-width="1.5" {i}/>
""",
    "doubt": """
<circle cx="36" cy="36" r="22" stroke-width="2.0" {i}/>
<path d="M29 30c1-6 10-7 13-2 3 5-3 7-6 10-2 2-2 4-2 6M34 50v1" stroke-width="1.8" {i}/>
<path d="M16 16l4 4M56 16l-4 4" stroke-width="1.1" {i}/>
""",
    "anger": """
<circle cx="36" cy="37" r="20" stroke-width="2.0" {i}/>
<path d="M22 29l10 4M50 29l-10 4M27 46c6 5 12 5 18 0" stroke-width="1.8" {i}/>
<path d="M13 16l5 5M59 16l-5 5M18 10l2 5M54 10l-2 5" stroke-width="1.25" {i}/>
""",
    "four": """
<path d="M48 12v48M48 12L17 43h42" stroke-width="2.25" {i}/>
<path d="M17 43c6-1 11-1 17 0" stroke-width="1.15" {i}/>
""",
    "nine": """
<path d="M48 38c-4 8-12 12-20 9-8-3-11-11-7-19 4-8 14-11 22-7 8 4 10 14 5 25-4 9-10 14-19 16" stroke-width="2.2" {i}/>
<path d="M24 27c5 3 11 3 17 0" stroke-width="1.15" {i}/>
""",
    "planet": """
<circle cx="36" cy="36" r="15" stroke-width="2.05" {i}/>
<path d="M10 43c13-8 29-10 52-2 3 1 3 4 0 5-16 5-35 4-52-3z" stroke-width="1.75" {i}/>
<path d="M28 24c4 3 8 3 12 1M42 42c3 2 5 4 6 7" stroke-width="1.15" {i}/>
""",
    "harm": """
<path d="M36 12c-4 7-7 13-7 19 0 7 3 11 7 11s7-4 7-11c0-6-3-12-7-19z" stroke-width="2.05" {i}/>
<path d="M16 54c7-6 14-6 20 0 6-6 13-6 20 0" stroke-width="1.75" {i}/>
<path d="M23 20l26 32M49 20L23 52" stroke-width="1.25" {i}/>
""",
    "architecture": """
<path d="M12 57h48M17 57V30h38v27M13 30l23-17 23 17z" stroke-width="2.1" {i}/>
<path d="M24 57V38M36 57V38M48 57V38M20 31h32" stroke-width="1.35" {i}/>
""",
    "experiment": """
<path d="M29 12h14M33 12v19L20 54c-2 4 2 7 7 7h18c5 0 9-3 7-7L39 31V12" stroke-width="2.0" {i}/>
<path d="M25 48c7-4 15-4 25 0M29 39h15" stroke-width="1.3" {i}/>
<circle cx="35" cy="45" r="2" stroke-width="1.0" {i}/>
""",
    "decay": """
<path d="M36 14c-10 1-17 9-17 20 0 12 7 22 17 25 10-3 17-13 17-25 0-11-7-19-17-20z" stroke-width="2.05" {i}/>
<path d="M29 22c4 5 5 10 2 15-3 5-2 10 3 16M44 24c-4 4-5 8-3 12 2 4 1 8-2 11" stroke-width="1.35" {i}/>
""",
    "death": """
<path d="M36 12c-13 0-22 10-22 23 0 8 5 13 10 15v8h24v-8c5-2 10-7 10-15 0-13-9-23-22-23z" stroke-width="2.1" {i}/>
<path d="M25 31l7 5M47 31l-7 5M27 47c6-3 12-3 18 0M32 58v-5M40 58v-5" stroke-width="1.65" {i}/>
""",
    "past": """
<circle cx="32" cy="34" r="20" stroke-width="2.1" {i}/>
<path d="M32 20v15l9 7M15 19l-5 5M10 24h7" stroke-width="1.55" {i}/>
<path d="M46 48c7 2 10 7 10 13M56 61l-1-5-5 2" stroke-width="1.25" {i}/>
""",
    "empire": """
<path d="M14 55h44M18 55V31h36v24M13 31l8-13 15 9 15-9 8 13z" stroke-width="2.1" {i}/>
<path d="M25 55V40M36 55V40M47 55V40M20 31h32" stroke-width="1.35" {i}/>
""",
    "if": """
<path d="M14 22c8-7 16-7 22 0 6 7 14 7 22 0M14 50c8-7 16-7 22 0 6 7 14 7 22 0" stroke-width="2.05" {i}/>
<path d="M36 22v28M30 35l6 6 6-6" stroke-width="1.4" {i}/>
""",
    "east": """
<path d="M36 14v38M13 36h46" stroke-width="1.15" {i}/>
<path d="M36 52c-10-1-17-8-17-17 0-10 7-17 17-18 10 1 17 8 17 18 0 9-7 16-17 17z" stroke-width="1.95" {i}/>
<path d="M36 17l-4 6M36 17l4 6" stroke-width="1.2" {i}/>
""",
    "hope": """
<path d="M36 59V34M36 43c-8-7-15-8-21-4 3 8 10 12 21 11M36 39c7-8 14-9 21-5-3 8-10 12-21 12" stroke-width="2.0" {i}/>
<path d="M36 22l2 5M31 25l5-3 5 3" stroke-width="1.25" {i}/>
<path d="M13 61c14-3 30-3 46 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "measure": """
<path d="M14 24h44v28H14z" stroke-width="2.0" {i}/>
<path d="M22 24v8M30 24v5M38 24v8M46 24v5M54 24v8" stroke-width="1.25" {i}/>
<path d="M22 39h24" stroke-width="1.35" {i}/>
""",
    "destiny": """
<path d="M36 12l5 15 16 1-12 10 4 16-13-8-14 8 5-16-13-10 16-1z" stroke-width="1.85" {i}/>
<path d="M36 42v17M30 52l6 7 6-7" stroke-width="1.25" {i}/>
""",
    "joy": """
<circle cx="36" cy="34" r="18" stroke-width="2.0" {i}/>
<path d="M24 31c3-3 6-3 9 0M39 31c3-3 6-3 9 0M25 42c7 6 15 6 22 0" stroke-width="1.75" {i}/>
<path d="M36 10v6M18 16l4 4M54 16l-4 4" stroke-width="1.15" {i}/>
""",
    "habitat": """
<path d="M12 56c8-12 16-18 24-18s16 6 24 18" stroke-width="2.1" {i}/>
<path d="M20 51c5-7 10-10 16-10s11 3 16 10" stroke-width="1.55" {i}/>
<path d="M36 41c-5-7-5-13 0-19 5 6 5 12 0 19z" stroke-width="1.45" {i}/>
""",
    "performance": """
<path d="M13 18h46M13 18v40M59 18v40M13 58h46" stroke-width="1.75" {i}/>
<path d="M21 18c7 8 7 17 0 27M51 18c-7 8-7 17 0 27" stroke-width="1.45" {i}/>
<path d="M28 52c4-8 12-8 16 0M36 45v-8M31 39l5-4 5 4" stroke-width="1.6" {i}/>
""",
    "fear": """
<path d="M36 15c-8 0-14 6-14 14 0 7 4 12 10 14v13h8V43c6-2 10-7 10-14 0-8-6-14-14-14z" stroke-width="2.05" {i}/>
<path d="M29 31l5 3M43 31l-5 3M32 40c3-2 5-2 8 0" stroke-width="1.55" {i}/>
<path d="M17 17l4 4M55 17l-4 4" stroke-width="1.15" {i}/>
""",
    "effect": """
<circle cx="36" cy="36" r="7" stroke-width="1.8" {i}/>
<path d="M36 11v12M36 49v12M11 36h12M49 36h12M18 18l8 8M46 46l8 8M54 18l-8 8M26 46l-8 8" stroke-width="1.55" {i}/>
<path d="M32 36l3 3 7-8" stroke-width="1.35" {i}/>
""",
    "care": """
<path d="M36 56C24 48 15 41 15 30c0-7 9-11 15-4l6 7 6-7c6-7 15-3 15 4 0 11-9 18-21 26z" stroke-width="2.15" {i}/>
<path d="M23 25c3-3 7-3 10 0M49 25c-3-3-7-3-10 0" stroke-width="1.15" {i}/>
""",
    "melt": """
<path d="M21 15h30l-4 18c-1 5-5 9-11 12-6-3-10-7-11-12z" stroke-width="2.1" {i}/>
<path d="M36 45c-6 7-9 11-9 15 0 5 4 8 9 8s9-3 9-8c0-4-3-8-9-15z" stroke-width="1.85" {i}/>
<path d="M28 22h16M30 29h12" stroke-width="1.0" opacity=".7" {i}/>
""",
    "globe": """
<circle cx="36" cy="36" r="23" stroke-width="2.2" {i}/>
<path d="M22 20c5 3 9 7 9 12-1 5-6 7-7 12-1 4 3 8 7 10M45 16c-2 6-1 11 4 14 4 3 4 8 0 12-3 3-4 7-2 12M14 37c7-3 14-3 21 0 8 4 15 4 23 0" stroke-width="1.5" {i}/>
""",
    "evening": """
<path d="M49 14c-9 2-15 10-15 19 0 11 8 19 19 19 4 0 8-1 11-3-4 7-11 11-20 11-14 0-24-10-24-23 0-13 11-23 24-23 2 0 3 0 5 0z" stroke-width="2.1" {i}/>
<path d="M10 58c9-4 18-4 27 0 8 4 16 4 25 0M18 16l1 3M60 24l1 3" stroke-width="1.2" {i}/>
""",
    "nutrition": """
<path d="M14 31h44l-4 22c-1 6-8 9-18 9s-17-3-18-9z" stroke-width="2.1" {i}/>
<path d="M14 31c4-8 12-12 22-12s18 4 22 12c-10 4-34 4-44 0z" stroke-width="1.75" {i}/>
<path d="M36 19c-2-7 2-11 8-13M36 20c-6-5-11-4-15 1M31 23c2-5 6-7 11-6" stroke-width="1.25" {i}/>
""",
    "morning": """
<path d="M12 51c8-7 16-7 24 0 8-7 16-7 24 0" stroke-width="2.0" {i}/>
<path d="M20 48c0-10 7-18 16-18s16 8 16 18" stroke-width="1.75" {i}/>
<path d="M36 12v10M18 20l6 6M54 20l-6 6M10 31h10M62 31H52" stroke-width="1.3" {i}/>
""",
    "labor": """
<circle cx="27" cy="18" r="5" stroke-width="1.75" {i}/>
<path d="M25 24c-3 7-3 14 1 21 3 5 7 7 11 7M29 29c-4 3-8 8-10 13M31 29c6 2 10 6 13 11M37 52c-5 2-10 5-14 9M37 52c4 3 7 6 9 10" stroke-width="1.95" {i}/>
<path d="M43 40l13-20M52 18l6 3M52 18l-2 7" stroke-width="1.55" {i}/>
<path d="M10 62c14-3 31-3 52 0" stroke-width="1.0" opacity=".65" {i}/>
""",
    "expression": """
<path d="M36 12c-13 0-22 9-22 22 0 13 9 22 22 22s22-9 22-22c0-13-9-22-22-22z" stroke-width="2.1" {i}/>
<path d="M23 30c4-3 8-3 12 0M49 30c-4-3-8-3-12 0M25 46c7 5 15 5 22 0" stroke-width="1.7" {i}/>
<path d="M36 35v5" stroke-width="1.2" {i}/>
""",
    "metaphor": """
<path d="M12 53c8-20 17-29 24-29s16 9 24 29" stroke-width="2.1" {i}/>
<path d="M12 53h48M21 53c5-11 10-17 15-17s10 6 15 17" stroke-width="1.45" {i}/>
<path d="M36 24V12M31 17l5-5 5 5" stroke-width="1.2" {i}/>
""",
}


def redraw(name: str, body: str) -> None:
    path = OUT / f"{name}.svg"
    original = path.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA code point: {path}")
    label = f"science / {name}"
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {cp.group(0)} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1">\n'
        f'<title>{label} — simplified naturalist study</title>{body.format(i=INK)}</svg>\n'
    )
    path.write_text(svg)


for name, body in ART.items():
    redraw(name, body)
print(f"redrew {len(ART)} science studies")
