import logging

import pytest

import kopf
from kopf.reactor.causation import ChangingCause
from kopf.reactor.indexing import OperatorIndexers
from kopf.storage.states import State
from kopf.structs.bodies import Body
from kopf.structs.ephemera import Memo
from kopf.structs.handlers import Reason
from kopf.structs.patches import Patch


@pytest.mark.parametrize('lifecycle', [
    kopf.lifecycles.all_at_once,
    kopf.lifecycles.one_by_one,
    kopf.lifecycles.randomized,
    kopf.lifecycles.shuffled,
    kopf.lifecycles.asap,
])
async def test_protocol_invocation(lifecycle, resource):
    """
    To be sure that all kwargs are accepted properly.
    Especially when the new kwargs are added or an invocation protocol changed.
    """
    # The values are irrelevant, they can be anything.
    state = State.from_scratch()
    cause = ChangingCause(
        logger=logging.getLogger('kopf.test.fake.logger'),
        indices=OperatorIndexers().indices,
        resource=resource,
        patch=Patch(),
        memo=Memo(),
        body=Body({}),
        initial=False,
        reason=Reason.NOOP,
    )
    handlers = []
    selected = lifecycle(handlers, state=state, **cause.kwargs)
    assert isinstance(selected, (tuple, list))
    assert len(selected) == 0
