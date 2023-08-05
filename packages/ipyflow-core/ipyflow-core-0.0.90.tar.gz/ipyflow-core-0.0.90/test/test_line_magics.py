# -*- coding: utf-8 -*-
import textwrap

from ipyflow.data_model.code_cell import cells

from ipyflow.line_magics import _USAGE
from ipyflow.run_mode import FlowDirection, ExecutionMode, ExecutionSchedule
from ipyflow.singletons import kernel, flow
from ipyflow.tracing.ipyflow_tracer import DataflowTracer
from test.utils import make_flow_fixture

# Reset dependency graph before each test
_flow_fixture, run_cell_ = make_flow_fixture()


def run_cell(cell, **kwargs):
    # print()
    # print('*******************************************')
    # print('running', cell)
    # print('*******************************************')
    # print()
    run_cell_(cell, **kwargs)


def test_show_usage():
    run_cell("%flow not_a_real_subcommand")
    cell1 = cells().from_id(1)
    assert cell1.captured_output.stderr.strip() == _USAGE.strip(), (
        "got %s" % cell1.captured_output.stderr
    )


def test_toggle_dataflow():
    assert flow().mut_settings.dataflow_enabled
    run_cell("%flow disable")
    assert not flow().mut_settings.dataflow_enabled
    run_cell("%flow enable")
    assert flow().mut_settings.dataflow_enabled


def test_show_deps_show_waiting():
    run_cell("x = 0")
    run_cell("y = x + 1")
    run_cell("logging.info(y)")
    run_cell("%flow show_deps y")
    cell4 = cells().from_id(4)
    assert (
        cell4.captured_output.stdout.strip()
        == "Symbol y (defined cell: 2; last updated cell: 2) is dependent on {<x>} and is a parent of nothing"
    ), ("got %s" % cell4.captured_output)
    run_cell("%flow show_waiting")
    cell5 = cells().from_id(5)
    assert (
        cell5.captured_output.stdout.strip()
        == "No symbol waiting on dependencies for now!"
    ), ("got %s" % cell5.captured_output)
    run_cell("x = 42")
    run_cell("%flow show_waiting")
    cell7 = cells().from_id(7)
    assert (
        cell7.captured_output.stdout.strip()
        == "Symbol(s) waiting on dependencies: {<y>}"
    ), ("got %s" % cell7.captured_output)
    run_cell("y = x + 1")
    run_cell("%flow show_waiting")
    cell9 = cells().from_id(9)
    assert (
        cell9.captured_output.stdout.strip()
        == "No symbol waiting on dependencies for now!"
    ), ("got %s" % cell9.captured_output)


def test_enable_disable_trace_messages():
    assert not flow().trace_messages_enabled
    run_cell("%flow trace_messages enable")
    assert flow().trace_messages_enabled
    run_cell("%flow trace_messages disable")
    assert not flow().trace_messages_enabled


def test_enable_disable_highlights():
    assert flow().mut_settings.highlights_enabled
    run_cell("%flow nohls")
    assert not flow().mut_settings.highlights_enabled
    run_cell("%flow hls")
    assert flow().mut_settings.highlights_enabled
    run_cell("%flow highlights off")
    assert not flow().mut_settings.highlights_enabled
    run_cell("%flow highlights on")
    assert flow().mut_settings.highlights_enabled
    run_cell("%flow highlights disable")
    assert not flow().mut_settings.highlights_enabled
    run_cell("%flow highlights enable")


def test_make_slice():
    run_cell("x = 0")
    run_cell("y = x + 1")
    run_cell("x = 42")
    run_cell("logging.info(y)")
    run_cell("%flow slice 4")
    cell5 = cells().from_id(5)
    assert (
        cell5.captured_output.stdout.strip()
        == textwrap.dedent(
            """
        # Cell 1
        x = 0
        
        # Cell 2
        y = x + 1
        
        # Cell 4
        logging.info(y)
        """
        ).strip()
    ), ("got %s" % cell5.captured_output)


def test_set_exec_mode():
    assert flow().mut_settings.exec_mode == ExecutionMode.NORMAL
    run_cell(f"%flow mode {ExecutionMode.REACTIVE.value}")
    assert flow().mut_settings.exec_mode == ExecutionMode.REACTIVE
    run_cell(f"%flow mode {ExecutionMode.NORMAL.value}")
    assert flow().mut_settings.exec_mode == ExecutionMode.NORMAL


def test_set_exec_schedule_and_flow_order():
    assert flow().mut_settings.exec_schedule == ExecutionSchedule.LIVENESS_BASED
    run_cell(f"%flow direction {FlowDirection.IN_ORDER.value}")
    assert flow().mut_settings.flow_order == FlowDirection.IN_ORDER
    for schedule in ExecutionSchedule:
        run_cell(f"%flow schedule {schedule.value}")
        assert flow().mut_settings.exec_schedule == schedule
    run_cell(f"%flow schedule {ExecutionSchedule.LIVENESS_BASED.value}")
    assert flow().mut_settings.exec_schedule == ExecutionSchedule.LIVENESS_BASED
    run_cell(f"%flow direction {FlowDirection.ANY_ORDER.value}")
    assert flow().mut_settings.flow_order == FlowDirection.ANY_ORDER
    run_cell(f"%flow schedule {ExecutionSchedule.STRICT.value}")
    # strict schedule only works for in_order semantics
    assert flow().mut_settings.exec_schedule == ExecutionSchedule.LIVENESS_BASED


def test_register_deregister_tracer():
    assert DataflowTracer in kernel().registered_tracers
    run_cell(f"%flow deregister {DataflowTracer.__module__}.{DataflowTracer.__name__}")
    assert DataflowTracer not in kernel().registered_tracers
    run_cell(f"%flow register {DataflowTracer.__module__}.{DataflowTracer.__name__}")
    assert DataflowTracer in kernel().registered_tracers


def test_clear():
    run_cell("%flow clear")
    assert flow().min_timestamp == flow().cell_counter()
    run_cell("x = 42")
    assert flow().min_timestamp == flow().cell_counter() - 1
    run_cell("%flow clear")
    assert flow().min_timestamp == flow().cell_counter()


def test_tags():
    run_cell("%flow tag foo")
    cell1 = cells().current_cell()
    assert cell1 is cells().from_counter(1)
    assert cell1.tags == ("foo",)
    run_cell("%flow show_tags --cell 1")
    assert (
        cells().current_cell().captured_output.stdout.strip()
        == "Cell has tags: ('foo',)"
    )
    run_cell("%flow tag --remove foo --cell 1")
    assert cells().from_counter(1).tags == ()
    run_cell("%flow show-tags --cell 1")
    assert cells().current_cell().captured_output.stdout.strip() == "Cell has tags: ()"
