from langchain.agents.middleware import ModelCallLimitMiddleware

from configs.server_config import MAX_MODEL_CALLS_PER_RUN


def build_middlewares(
    *,
    enable_hitl: bool
) -> list:
    layers: list = [
        ModelCallLimitMiddleware(
            run_limit=MAX_MODEL_CALLS_PER_RUN,
            exit_behavior="end"
        )
    ]

    # if enable_hitl:
    #     layers.append(build_hitl_middleware())

    return layers