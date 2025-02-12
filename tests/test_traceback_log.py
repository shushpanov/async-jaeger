import mock
from async_jaeger import Span, SpanContext


def test_traceback():
    """Test that a traceback is logged with both location and message"""
    mock_tracer = mock.MagicMock()
    mock_tracer.max_tag_value_length = 300
    mock_tracer.max_traceback_length = 300
    context = SpanContext(trace_id=1, span_id=2, parent_id=None, flags=1)
    span = Span(context=context, operation_name='traceback_test', tracer=mock_tracer)

    try:
        with span:
            raise ValueError('Something unexpected happened!')
    except ValueError:
        fields_dict = {field.key: field.vStr for field in span.logs[0].fields}
        assert 'stack' in fields_dict
        stack_message = fields_dict['stack']
        stack_message_lines = stack_message.splitlines()
        assert len(stack_message_lines) == 2
        assert stack_message_lines[0].startswith('  File ')
        assert stack_message_lines[1] == \
            "    raise ValueError('Something unexpected happened!')"


def test_traceback_cut():
    """Test that a traceback is cut off at max_tag_value_length"""
    mock_tracer = mock.MagicMock()
    mock_tracer.max_tag_value_length = 300
    mock_tracer.max_traceback_length = 5
    context = SpanContext(trace_id=1, span_id=2, parent_id=None, flags=1)
    span = Span(context=context, operation_name='traceback_test', tracer=mock_tracer)

    try:
        with span:
            raise ValueError('Something unexpected happened!')
    except ValueError:
        fields_dict = {field.key: field.vStr for field in span.logs[0].fields}
        assert 'stack' in fields_dict
        stack_message = fields_dict['stack']
        assert stack_message == '  Fil'
