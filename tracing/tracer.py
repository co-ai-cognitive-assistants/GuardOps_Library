import pytz
import datetime
from tracing.custom_processor import JSONProcessor, process_response
from dotenv import load_dotenv
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from traceloop.sdk import Traceloop
from phoenix.trace.langchain import OpenInferenceTracer
from typing import Any



load_dotenv(override=True)
pytz.timezone('Europe/Berlin').localize(datetime.datetime.utcnow())


#to fix tracing, ctrl+click on openinferencetracer, then comment out the on_chat_model_start lines like below
# @graceful_fallback(_chat_model_start_fallback)
#     def on_chat_model_start(
#         self,
#         serialized: Dict[str, Any],
#         messages: List[List[BaseMessage]],
#         *,
#         run_id: UUID,
#         tags: Optional[List[str]] = None,
#         parent_run_id: Optional[UUID] = None,
#         metadata: Optional[Dict[str, Any]] = None,
#         name: Optional[str] = None,
#         **kwargs: Any,
#     ) -> None:
#         """
#         Adds chat messages to the run inputs.

#         LangChain's BaseTracer class does not implement hooks for chat models and hence does not
#         record data such as the list of messages that were passed to the chat model.

#         For reference, see https://github.com/langchain-ai/langchain/pull/4499.
#         """

#         parent_run_id_ = str(parent_run_id) if parent_run_id else None
#         #execution_order = self._get_execution_order(parent_run_id_) ------- COMMENT HERE -------
#         start_time = datetime.utcnow()
#         if metadata:
#             kwargs.update({"metadata": metadata})
#         run = Run(
#             id=run_id,
#             parent_run_id=parent_run_id,
#             serialized=serialized,
#             inputs={"messages": [[dumpd(message) for message in batch] for batch in messages]},
#             extra=kwargs,
#             events=[{"name": "start", "time": start_time}],
#             start_time=start_time,
#             #execution_order=execution_order, ------- COMMENT HERE -------
#             #child_execution_order=execution_order, ------- COMMENT HERE -------
#             run_type="llm",
#             tags=tags,
#             name=name or "",
#         )
#         self._start_trace(run)
class Tracer(OpenInferenceTracer):

    
    def __init__(self,config, *args: Any, **kwargs: Any) -> None:
        self.resource = Resource(attributes={
                SERVICE_NAME: "llm-tracing"
                })
        self.tracer_provider = TracerProvider(resource=self.resource)
        self.config = config
        span_exporter = SpanExporter()
        processor = JSONProcessor(config=self.config, span_exporter=SpanExporter())
        self.tracer_provider.add_span_processor(span_processor=processor)
        #OpenLLMetry tracer
        Traceloop.init(exporter=span_exporter, processor=processor,traceloop_sync_enabled=False)
        super().__init__(*args, **kwargs)
       