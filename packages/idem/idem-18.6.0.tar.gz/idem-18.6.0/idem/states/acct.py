import dict_tools.differ as differ
import dict_tools.update

__func_alias__ = {"profile_": "profile"}


async def profile_(
    hub,
    ctx,
    name: str,
    provider_name: str,
    profile_name: str = None,
    **kwargs,
):
    """
    :param hub:
    :param ctx:
    :param name: The name of the profile to add to acct
    :param provider_name: The name of the provider that this profile should be used for
    :param profile_name: The name of the new profile to add, defaults to the state name
    :param kwargs: Any extra keyword arguments will be passed directly into the new profile

    Extend the profiles of the current run with information passed to this state.
    The goal is not to write your acct_file for you with automation;.
    The purpose of this state is to dynamically create credentials for things like assuming new roles
      -- which can be re-calculated every run with negligible overhead.

    .. code-block:: yaml

        state_name:
          acct.profile:
            - provider_name: test
            - profile_name: default
            - key_1: value_1
            - key_2: value_2
    """
    result = dict(comment=[], changes=None, name=name, result=True)
    if "profiles" not in hub.idem.RUNS[ctx.run_name]["acct_data"]:
        hub.idem.RUNS[ctx.run_name]["acct_data"]["profiles"] = {}

    before = (
        hub.idem.RUNS[ctx.run_name]["acct_data"]["profiles"]
        .get(provider_name, {})
        .keys()
    )

    if profile_name is None:
        profile_name = name

    # Verify that we are not overwriting an existing profile unless explicitly asked to
    if profile_name in hub.idem.RUNS[ctx.run_name]["acct_data"]["profiles"].get(
        provider_name, {}
    ):
        result["comment"] += [
            f"Overwriting '{profile_name}' under provider '{provider_name}'"
        ]

    # Create a new raw profile
    profiles = {provider_name: {profile_name: kwargs}}

    # Run the profiles through the gather plugins and update them with any changes
    processed_profiles = await hub.acct.init.process([provider_name], profiles)
    dict_tools.update.update(profiles, processed_profiles)

    # Update the profiles in the RUNS structure
    if ctx.test:
        after = profiles.get(provider_name, {}).keys()
        result["comment"] += [
            f"Would add {provider_name} profiles to the internal RUNS structure"
        ]
    else:
        dict_tools.update.update(
            hub.idem.RUNS[ctx.run_name]["acct_data"]["profiles"], profiles
        )
        # Return the only profile keys that have been changed for this state since the values contain secure information
        after = (
            hub.idem.RUNS[ctx.run_name]["acct_data"]["profiles"]
            .get(provider_name, {})
            .keys()
        )

    # Calculate changes directly to prevent sending a new_state to ESM
    result["changes"] = differ.deep_diff(
        {"profiles": list(before)}, {"profiles": list(after)}
    )

    return result
