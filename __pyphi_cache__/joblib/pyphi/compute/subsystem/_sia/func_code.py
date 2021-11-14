# first line: 1
@memory.cache(ignore=["subsystem"])
@time_annotated
def _sia(cache_key, subsystem):
    """Return the minimal information partition of a subsystem.

    Args:
        subsystem (Subsystem): The candidate set of nodes.

    Returns:
        SystemIrreducibilityAnalysis: A nested structure containing all the
        data from the intermediate calculations. The top level contains the
        basic irreducibility information for the given subsystem.
    """
    # pylint: disable=unused-argument

    log.info('Calculating big-phi data for %s...', subsystem)

    # Check for degenerate cases
    # =========================================================================
    # Phi is necessarily zero if the subsystem is:
    #   - not strongly connected;
    #   - empty;
    #   - an elementary micro mechanism (i.e. no nontrivial bipartitions).
    # So in those cases we immediately return a null SIA.
    if not subsystem:
        log.info('Subsystem %s is empty; returning null SIA '
                 'immediately.', subsystem)
        return _null_sia(subsystem)

    if not connectivity.is_strong(subsystem.cm, subsystem.node_indices):
        log.info('%s is not strongly connected; returning null SIA '
                 'immediately.', subsystem)
        return _null_sia(subsystem)

    # Handle elementary micro mechanism cases.
    # Single macro element systems have nontrivial bipartitions because their
    #   bipartitions are over their micro elements.
    if len(subsystem.cut_indices) == 1:
        # If the node lacks a self-loop, phi is trivially zero.
        if not subsystem.cm[subsystem.node_indices][subsystem.node_indices]:
            log.info('Single micro nodes %s without selfloops cannot have '
                     'phi; returning null SIA immediately.', subsystem)
            return _null_sia(subsystem)
        # Even if the node has a self-loop, we may still define phi to be zero.
        elif not config.SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI:
            log.info('Single micro nodes %s with selfloops cannot have '
                     'phi; returning null SIA immediately.', subsystem)
            return _null_sia(subsystem)
    # =========================================================================

    log.debug('Finding unpartitioned CauseEffectStructure...')
    unpartitioned_ces = _ces(subsystem)

    if not unpartitioned_ces:
        log.info('Empty unpartitioned CauseEffectStructure; returning null '
                 'SIA immediately.')
        # Short-circuit if there are no concepts in the unpartitioned CES.
        return _null_sia(subsystem)

    log.debug('Found unpartitioned CauseEffectStructure.')

    # TODO: move this into sia_bipartitions?
    # Only True if SINGLE_MICRO_NODES...=True, no?
    if len(subsystem.cut_indices) == 1:
        cuts = [Cut(subsystem.cut_indices, subsystem.cut_indices,
                    subsystem.cut_node_labels)]
    else:
        cuts = sia_bipartitions(subsystem.cut_indices,
                                subsystem.cut_node_labels)

    engine = ComputeSystemIrreducibility(
        cuts, subsystem, unpartitioned_ces)
    result = engine.run(config.PARALLEL_CUT_EVALUATION)

    if config.CLEAR_SUBSYSTEM_CACHES_AFTER_COMPUTING_SIA:
        log.debug('Clearing subsystem caches.')
        subsystem.clear_caches()

    log.info('Finished calculating big-phi data for %s.', subsystem)

    return result
