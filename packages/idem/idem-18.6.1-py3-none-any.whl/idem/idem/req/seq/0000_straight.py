from typing import Any
from typing import Dict


def run(
    hub,
    seq: Dict[int, Dict[str, Any]],
    low: Dict[str, Any],
    running: Dict[str, Any],
    options: Dict[str, Any],
) -> Dict[int, Dict[str, Any]]:
    """
    Return the sequence map that should be used to execute the lowstate
    The sequence needs to identify:
    1. recursive requisites
    2. what chunks are free to run
    3. Behavior augments for the next chunk to run
    """
    ret = {}
    for ind, chunk in enumerate(low):
        tag = hub.idem.tools.gen_tag(chunk)
        if tag in running:
            # Already ran this one, don't add it to the sequence
            continue
        ret[ind] = {
            "chunk": chunk,
            "reqrets": [],
            "unmet": set(),
            "tag": tag,
            "errors": [],
        }
        for req, data in hub.idem.RMAP.items():
            if data.get("prereq"):
                continue
            if req in chunk:
                for rdef in chunk[req]:
                    if not isinstance(rdef, dict):
                        # TODO: Error check
                        continue
                    state = next(iter(rdef))
                    if isinstance(rdef[state], list):
                        name_defs = rdef[state]
                    else:
                        name_defs = [{rdef[state]: []}]

                    for name_def in name_defs:
                        if not isinstance(name_def, dict):
                            # TODO: Error check
                            continue
                        name = next(iter(name_def))
                        args = name_def[name]
                        r_chunks = hub.idem.tools.get_chunks(low, state, name)
                        if not r_chunks:
                            ret[ind]["errors"].append(
                                f"Requisite {req} {state}:{name} not found"
                            )
                        # TODO: Can there ever be more than one chunk with the same cloud and name?
                        for r_chunk in r_chunks:
                            r_tag = hub.idem.tools.gen_tag(r_chunk)
                            if r_tag in running:
                                reqret = {
                                    "req": req,
                                    "name": name,
                                    "state": state,
                                    "r_tag": r_tag,
                                    "ret": running[r_tag],
                                    "chunk": "r_chunk",
                                    "args": args,
                                }
                                # it has been run, check the rules
                                ret[ind]["reqrets"].append(reqret)
                            else:
                                ret[ind]["unmet"].add(r_tag)
    return ret
