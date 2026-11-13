"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    pro, con = await asyncio.gather(
        agent.ask('advocate', 'Argue for a bounded pilot using only this evidence.', data, 'Pilot for six weeks with staggered support coverage.'),
        agent.ask('skeptic', 'Identify risks using only this evidence.', data, 'Coverage gaps and workload compression need measurement.'))
    rebuttal = await agent.ask('rebuttal', 'Respond to both positions and identify unresolved evidence needs.', {'pro': pro, 'con': con}, 'Measure coverage and workload; the evidence does not yet prove a benefit.')
    decision = await agent.ask('moderator', 'Return a decision and unresolved questions, not a claim of universal agreement.', {'pro': pro, 'con': con, 'rebuttal': rebuttal},
                               {'decision': 'pilot_with_conditions', 'unresolved': ['Coverage impact', 'Workload change']})
    return {'positions': {'pro': pro, 'con': con}, 'rebuttal': rebuttal, 'decision': decision}
