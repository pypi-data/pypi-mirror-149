from helios.defaults import DEFAULT_HS_API_ENDPOINT
from helios.instrumentation.base import HeliosBaseInstrumentor
import logging
import json

from opentelemetry.trace import (
    INVALID_SPAN,
    INVALID_SPAN_CONTEXT,
    get_current_span,
)


class HeliosLoggingInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.logging'
    INSTRUMENTOR_NAME = 'LoggingInstrumentor'

    _old_factory = None

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider)

        self._inject_context_to_record_message()

    def uninstrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        if self._old_factory:
            logging.setLogRecordFactory(self._old_factory)
            self._old_factory = None

        self.get_instrumentor().uninstrument(tracer_provider=tracer_provider)

    def _inject_context_to_record_message(self):
        old_factory = logging.getLogRecordFactory()
        self._old_factory = old_factory

        def _inject_otel_context_to_log_msg(record, message_as_json):
            if "otelSpanID" not in message_as_json and hasattr(record, 'otelSpanID'):
                message_as_json.setdefault("otelSpanID", record.otelSpanID)
            if "otelTraceID" not in message_as_json and hasattr(record, 'otelTraceID'):
                message_as_json.setdefault("otelTraceID", record.otelTraceID)
                go_to_helios_url = f'{DEFAULT_HS_API_ENDPOINT}?actionTraceId={record.otelTraceID}'
                record.go_to_helios = go_to_helios_url
                message_as_json.setdefault("go_to_helios", go_to_helios_url)
            if "otelServiceName" not in message_as_json and hasattr(record, 'otelServiceName'):
                message_as_json.setdefault("otelServiceName", record.otelServiceName)
            return message_as_json

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)

            span = get_current_span()
            if span != INVALID_SPAN:
                ctx = span.get_span_context()
                if ctx != INVALID_SPAN_CONTEXT:
                    try:
                        if type(record.msg) is dict:
                            record.msg = _inject_otel_context_to_log_msg(record, record.msg)
                        elif isinstance(record.msg, str):
                            message_as_json = json.loads(record.msg)
                            record.msg = json.dumps(_inject_otel_context_to_log_msg(record, message_as_json))
                        else:
                            return
                    except Exception as e:
                        pass
            return record

        logging.setLogRecordFactory(record_factory)
