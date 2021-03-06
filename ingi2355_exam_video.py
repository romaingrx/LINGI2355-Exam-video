#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 May 17, 23:18:19
@last modified : 2021 May 21, 17:53:45
"""

from manim import *
import numpy as np
from copy import deepcopy


def IncrementCounter(counter, value=1, circumscribe=False):
    dec_value = list(
        filter(lambda x: isinstance(x, DecimalNumber), counter.submobjects)
    )[0]
    cdtv = ChangeDecimalToValue(dec_value, dec_value.get_value() + value)
    if circumscribe:
        return [cdtv, Circumscribe(dec_value)]
    return cdtv


def CounterGiveTicket(counter, ticket, cpu, width=0.5, next_to=DOWN):
    ticket.next_to(counter.get_center(), IN, 0)
    ticket.generate_target()
    ticket.target.width = width
    ticket.target.next_to(cpu, next_to, SMALL_BUFF)
    return MoveToTarget(ticket)


def get_message_mobj(scale=0.25, opacity=1):
    message = SVGMobject("ressources/svg/message.svg")
    message.set_fill(WHITE, opacity=opacity)
    message.scale(scale)
    return message


def get_lock_mobj(scale=0.25, opacity=1):
    message = SVGMobject("ressources/svg/lock.svg")
    message.set_fill(RED, opacity=opacity)
    message.scale(scale)
    return message


def get_cpu_mobj(scale, color=None, name=None):
    cpu_mobj = SVGMobject("ressources/svg/cpu.svg")
    if color:
        cpu_mobj.set_fill(color, opacity=1)
    if scale:
        cpu_mobj.scale(scale)
    if name:
        name_text = (
            Text(str(name))
            .set_fill(BLACK, 1)
            .move_to(cpu_mobj)
            .shift((DOWN + RIGHT) * cpu_mobj.height / 10)
        )
        name_text.height = cpu_mobj.height / 4
        return VGroup(cpu_mobj, name_text)
    return cpu_mobj


def get_eyes(which):
    eyes = SVGMobject(f"ressources/svg/eyes/{which}.svg")
    return eyes


def add_eyes_on_cpu(cpu, which="angry", direction="left"):
    eyes = get_eyes(which)
    if direction.lower() in ["right"]:
        eyes.flip(UP)
    eyes.width = 0.85 * cpu.width
    eyes.move_to(cpu.get_center()).shift(cpu.height * UP / 3.5)
    return VGroup(deepcopy(cpu), eyes)


class Title(Scene):
    def construct(self):

        frame = Rectangle(
            width=0.85 * config.frame_width, height=0.8 * config.frame_height
        )

        this_is = Tex("This is the presentation of")
        this_is.next_to(frame.get_top(), DOWN, 0)

        paper_name = Tex(
            '"Advanced synchronization techniques \
                    for task-based runtime systems"'
        ).move_to(frame)
        paper_name.width = frame.width

        in_5_minutes = Tex("in 5 minutes...")
        in_5_minutes.next_to(frame.get_corner(DOWN + RIGHT), UP + LEFT, 0)

        paper_link = (
            Tex("https://dl.acm.org/doi/10.1145/3437801.3441601", color=BLUE)
            .scale(0.5)
            .next_to(frame.get_corner(DOWN + LEFT), UP + RIGHT, 0)
        )

        self.play(Write(this_is))
        self.wait()

        self.play(FadeIn(paper_name))

        self.wait()
        self.play(Write(in_5_minutes))

        self.wait()
        self.play(FadeIn(paper_link))

        self.wait()


class CoresEvolution(GraphScene):

    CPU_CORES = {
        2000: 1,
        2001: 2,
        2002: 1,
        2003: 2,
        2004: 2,
        2005: 4,
        2006: 4,
        2007: 4,
        2008: 8,
        2009: 8,
        2010: 12,
        2011: 16,
        2012: 16,
        2013: 24,
        2014: 24,
        2015: 36,
        2016: 36,
        2017: 64,
        2018: 64,
        2019: 128,
        2020: 128,
        2021: 128,
    }

    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_axis_label="Number of cores per CPU",
            x_axis_label="Years",
            y_label_position=0.2 * UP + RIGHT,
            y_min=0,
            y_max=129,
            x_min=1999,
            x_max=2021,
            y_labeled_nums=[1, 8, 16, 32, 64, 128],
            x_labeled_nums=np.arange(2000, 2021, 10, dtype=np.uint32),
            graph_origin=3 * DOWN + 4 * LEFT,
            **kwargs,
        )

    def construct(self):
        from scipy.optimize import curve_fit

        self.setup_axes(animate=True)

        X = np.array(list(CoresEvolution.CPU_CORES.keys()))
        y = np.array(list(CoresEvolution.CPU_CORES.values()))

        [a, b], res1 = curve_fit(lambda x1, a, b: a * np.exp(b * (x1 - 2000)), X, y)

        func = lambda v: a * np.exp(b * (v - 2000))

        graph = self.get_graph(func, x_min=X[0], x_max=X[-1], y_max=128, color=ORANGE)

        for x, y in CoresEvolution.CPU_CORES.items():
            d = Dot(color=BLUE).move_to(self.coords_to_point(x, y))
            self.play(Create(d))
            self.wait(0)

        self.play(Create(graph))

        self.wait()


class PaperSummary(Scene):
    def construct(self):
        text_scale = 0.8

        frame = Rectangle(
            width=0.85 * config.frame_width, height=0.7 * config.frame_height
        )

        title = Text("Paper improvements").next_to(frame.get_top(), DOWN, 0)

        p01 = (
            Text("Wait-free data structure")
            .scale(text_scale)
            .next_to(frame.get_left(), RIGHT, 0)
            .shift(RIGHT + UP + 0.5 * DOWN)
        )
        p02 = (
            Text("Task scheduler based on delegation")
            .scale(text_scale)
            .next_to(frame.get_left(), RIGHT, 0)
            .shift(RIGHT + 1.5 * DOWN)
        )

        self.play(FadeIn(title))

        for p in (p01, p02):
            d = Dot(color=BLUE).next_to(p, LEFT, SMALL_BUFF)
            self.play(Write(p), Create(d))


class DataDependencies(Scene):
    def construct(self):
        code = """
int A = 42;
// '0x5628030aed40' <- &A

#pragma oss task in(A)
{
    #pragma oss task in(A)
}

#pragma oss task in(A)
{
    #pragma oss task in(A)
}
        """

        rendered_code = Code(
            code=code,
            tab_width=4,
            background="window",
            language="java",
            font="Monospace",
        )
        rendered_code.width = 5
        rendered_code.shift(4 * LEFT)

        y_code = rendered_code.get_coord(0)
        x_code = rendered_code.get_coord(1)
        width_code = rendered_code.width
        height_code = rendered_code.height

        self.play(Create(rendered_code), run_time=2)

        self.wait()

        # Arrow decleration
        def step_arrow():
            return rendered_code.line_spacing * DOWN

        def get_initial_arrow(**kwargs):
            dy = 0.0 * rendered_code.height * UP
            arrow = Arrow(start=RIGHT, end=LEFT, **kwargs)
            arrow.next_to(rendered_code, RIGHT)
            arrow.shift(-2 * step_arrow())
            return arrow

        def get_default_task(name, color, pos):
            circle = Circle(radius=0.5, color=color, fill_opacity=0.5)

            text = Text(name)

            circle_text = VGroup(circle, text)
            circle_text.arrange(IN)

            circle_text.move_to(pos)

            return circle_text

        def get_arrow_between_tasks(task1, task2, title):
            arrow = Arrow(task1, task2, buff=0)
            angle = arrow.get_angle()

            text = Text(title, size=0.4)
            to_shift = text.height

            text.move_to(arrow)

            text.shift(to_shift * UP)
            text.rotate(angle, about_point=arrow.get_center())
            start, end = arrow.get_start_and_end()
            vector = (end - start) / np.sum(end - start)
            text.shift(0.2 * np.array([-vector[0], vector[1], vector[2]]))

            arrow_text = VGroup(arrow, text)

            return arrow_text

        tasks_grid = [(2, 2), (5, 1), (2, -1), (5, -2)]
        tasks_pos = list(map(lambda g: g[0] * RIGHT + g[1] * UP, tasks_grid))

        arrow = get_initial_arrow(color=WHITE)

        parent1 = get_default_task("A", BLUE, tasks_pos[0])

        self.play(Create(parent1), Create(arrow), run_time=2)

        self.wait()

        child1 = get_default_task("A", ORANGE, tasks_pos[1])
        parent1_to_child1 = get_arrow_between_tasks(parent1, child1, "Child")

        arrow.generate_target()
        # arrow.target.set_fill(ORANGE, 1)
        arrow.target.shift(2 * step_arrow())

        self.play(
            MoveToTarget(arrow), Create(child1), Create(parent1_to_child1), run_time=2
        )

        self.wait()

        parent2 = get_default_task("A", BLUE, tasks_pos[2])
        parent1_to_parent2 = get_arrow_between_tasks(parent1, parent2, "Successor")

        # arrow.target.set_fill(BLUE, 1)
        arrow.target.shift(2 * step_arrow())

        self.play(
            MoveToTarget(arrow), Create(parent2), Create(parent1_to_parent2), run_time=2
        )

        self.wait()

        child2 = get_default_task("A", ORANGE, tasks_pos[3])
        parent2_to_child2 = get_arrow_between_tasks(parent2, child2, "Child")

        # arrow.target.set_fill(ORANGE, 1)
        arrow.target.shift(2 * step_arrow())

        self.play(
            MoveToTarget(arrow), Create(child2), Create(parent2_to_child2), run_time=2
        )

        self.wait()

        all_vec = (
            arrow,
            parent1,
            parent2,
            child1,
            child2,
            parent1_to_child1,
            parent2_to_child2,
            parent1_to_parent2,
        )

        self.play(
            *[Uncreate(v) for v in all_vec], rendered_code.animate.shift(7 * LEFT)
        )
        self.wait()


class ASMStates(Scene):
    def get_data_access_block(self, height=2.5, width=3.7, values=None):
        block = VGroup()
        rect = Rectangle(color=WHITE, height=height, width=width)
        h_line = Line(rect.get_left(), rect.get_right()).shift(0.3 * rect.height * UP)

        title_text = Text("DataAccess A")
        title_text.scale(0.7)
        title_text.set_color(BLUE)
        title_text.move_to(VGroup(h_line, VectorizedPoint(rect.get_top())))

        attrs_text = ["Type:", "Address:", "Successor:", "Child:", "Flags:"]

        attrs = Paragraph(*attrs_text, name="attributes")
        attrs.scale(0.5)
        attrs.next_to(h_line.get_left(), DOWN + RIGHT, buff=SMALL_BUFF)

        values_text = values or ["IN", "0x9F3B", "0x6DFF", "NULL", "0xFF24"]

        values = Paragraph(*values_text, name="values")
        values.scale(0.5)
        values.next_to(h_line.get_right(), DOWN + LEFT, buff=SMALL_BUFF)

        block.add(rect, h_line, title_text, attrs, values)

        return block

    def get_asm(self, width, height, name):
        asm = VGroup()

        rect = RoundedRectangle(color=BLUE, width=width, height=height)
        rect.set_fill(BLUE, opacity=0.05)

        name_asm = Text(name, color=BLUE)
        name_asm.scale(0.4)
        move_to = rect.get_center() + np.array([-rect.height / 2, rect.width / 2, 1])
        name_asm.next_to(rect.get_left() + rect.get_top(), DOWN + RIGHT, MED_SMALL_BUFF)

        asm.add(rect, name_asm)
        return asm

    def get_state(self, bits, radius=0.5, scale_text=0.2):
        circle = Circle(radius=radius, color=ORANGE, fill_opacity=0.5)

        text = Text(bits)
        text.move_to(circle)
        text.scale(scale_text)

        circle_text = VGroup(circle, text)

        return circle_text

    def construct(self):
        data_access_block = self.get_data_access_block()
        data_access_block.move_to(ORIGIN)

        self.play(Create(data_access_block), run_time=2)
        self.play(Circumscribe(data_access_block))
        self.wait()

        data_access_block.generate_target()
        data_access_block.target.shift(5.5 * LEFT + 2.5 * UP)
        data_access_block.target.scale(0.75)

        self.play(MoveToTarget(data_access_block), run_time=2)
        data_access_block = data_access_block.target

        asm = self.get_asm(
            0.9 * config.frame_width,
            0.45 * config.frame_height,
            "Atomic State Machine",
        )
        asm.shift(1.1 * DOWN)

        surr_flags = Rectangle(
            color=BLUE, width=0.95 * data_access_block.width, height=0.285
        ).move_to(data_access_block.get_center() + 0.58 * DOWN)
        surr_flags.set_fill(BLUE, opacity=0.25)

        self.play(Create(surr_flags), run_time=2)

        self.play(Transform(surr_flags, asm), run_time=2)

        arrow_messages = [
            None,
            "Read satisfied",
            "Task finished",
            "Successor registered",
            "Message ack",
        ]
        action_messages = [
            None,
            "Run task",
            None,
            "Send read satisfied\n      to successor",
            "Delete",
        ]

        radius = 0.5
        first_ = asm.get_left() + RIGHT
        last_ = asm.get_right() + LEFT
        dist_states = (last_ - first_) / 4

        states_group = VGroup()
        arrows_group = VGroup()
        actions_group = VGroup()
        for idx, (bits, arrow_message, action) in enumerate(
            zip(range(5), arrow_messages, action_messages)
        ):
            bits = "0b" + "0" * (4 - bits) + "1" * bits

            state = self.get_state(bits, scale_text=0.25, radius=radius).move_to(
                first_ + idx * dist_states
            )

            prev_state = (
                states_group.submobjects[-1] if len(states_group.submobjects) else None
            )

            if prev_state:
                arrow = Arrow(prev_state, state, color=WHITE, buff=0)
                text = Text(arrow_message)
                text.scale(0.3)
                text.next_to(arrow, UP, MED_LARGE_BUFF)
                # text.shift((dist_states - 2 * radius) * LEFT / 5)
                arrow_text_mobj = VGroup(arrow, text)

                self.play(Create(arrow_text_mobj))
                self.wait()

                arrows_group.add(arrow_text_mobj)

            self.play(Create(state))
            self.wait()

            if action:
                # theta = PI / 4
                action_mobj = Paragraph(*action.split("\n"), color=YELLOW)
                action_mobj.scale(0.3)
                action_mobj.next_to(state, DOWN, MED_LARGE_BUFF)
                # action_mobj.rotate(theta, about_point=state.get_center())

                self.play(Write(action_mobj))
                self.wait()
                actions_group.add(action_mobj)

            states_group.add(state)

        self.wait()

        messages_group = VGroup(*[get_message_mobj() for _ in arrows_group])
        for message, arrow in zip(messages_group, arrows_group):
            message.next_to(arrow, DOWN, SMALL_BUFF)
            message.shift(0.1 * LEFT + OUT)

        self.play(FadeIn(messages_group))
        self.wait()

        locks_group = VGroup()
        for arrow_mobj, message_mobj in zip(arrows_group, messages_group):
            lock_mobj = get_lock_mobj()
            lock_mobj.move_to(message_mobj.get_center())
            locks_group.add(lock_mobj)

        self.play(FadeIn(locks_group), FadeOut(messages_group))

        self.play(
            *[elem.animate.shift(config.frame_width * LEFT) for elem in self.mobjects]
        )

        self.wait()


class SchedulerWaitFree(Scene):
    def stack(self, mobj, num, title=None):
        stack = VGroup()
        for n in range(num):
            delta = (num - n - 1) * np.array([0.05, 0.05, -1])
            new_mobj = deepcopy(mobj)
            new_mobj.shift(delta)
            stack.add(new_mobj)

        if title:
            title_mobj = Text(title)
            title_mobj.width = 1.25 * stack.width
            title_mobj.next_to(stack, UP, SMALL_BUFF)
            stack.add(title_mobj)

        return stack

    def construct(self):
        _TOP = config.frame_height / 2 * UP
        _BOTTOM = -_TOP
        _RIGHT = config.frame_width / 2 * RIGHT
        _LEFT = -_RIGHT

        N_CPUS = 3
        H_SPACE = config.frame_width / 8
        MARGIN = config.frame_width / 7
        USABLE_WIDTH = config.frame_width - MARGIN
        COL_SPACE = (USABLE_WIDTH) / N_CPUS

        V_LINES = VGroup(
            Line(
                config.top + config.frame_width * LEFT / 2 + (MARGIN) * RIGHT,
                config.bottom + config.frame_width * LEFT / 2 + (MARGIN) * RIGHT,
            )
        )

        for _ in range(N_CPUS):
            new_line = deepcopy(V_LINES.submobjects[-1])
            V_LINES.add(new_line.shift(COL_SPACE * RIGHT))

        def get_center_col(idx):
            return VGroup(
                V_LINES.submobjects[idx], V_LINES.submobjects[idx + 1]
            ).get_center()

        def get_center_margin():
            return VGroup(
                Line(_TOP + _LEFT, _BOTTOM + _LEFT), V_LINES.submobjects[0]
            ).get_center()

        cpu_mobj = get_cpu_mobj(0.4)
        queue_mobj = Rectangle(width=0.33 * COL_SPACE, height=0.2 * config.frame_height)
        queue_mobj.set_fill(BLUE, opacity=0.5)

        creators_group = VGroup()
        queues_group = VGroup()
        arrows_group = VGroup()
        for cpu_idx in range(N_CPUS):
            curr_cpu_mobj = deepcopy(cpu_mobj)
            curr_cpu_mobj.move_to(get_center_col(cpu_idx))
            curr_cpu_mobj.shift(_TOP + (MED_SMALL_BUFF + curr_cpu_mobj.height) * DOWN)
            creators_group.add(curr_cpu_mobj)

            curr_queue_mobj = deepcopy(queue_mobj)
            curr_queue_mobj.next_to(curr_cpu_mobj, DOWN, MED_LARGE_BUFF)
            queues_group.add(curr_queue_mobj)

            arrow = Arrow(
                curr_cpu_mobj.get_center() + curr_cpu_mobj.height * DOWN / 2,
                curr_queue_mobj.get_center() + curr_queue_mobj.height * UP / 2,
                buff=0,
            )
            arrows_group.add(arrow)

        text_scale = 0.4
        text_color = WHITE
        margin_texts_group = VGroup()
        creator_mobj = (
            (Text("Creator\nThreads").scale(text_scale).set_fill(text_color, opacity=1))
            .move_to(get_center_margin())
            .shift(creators_group.get_center() * UP)
        )
        margin_texts_group.add(creator_mobj)

        queue_mobj = (
            (Text("Thread\nQueues").scale(text_scale).set_fill(text_color, opacity=1))
            .move_to(get_center_margin())
            .shift(queues_group.get_center() * UP)
        )
        margin_texts_group.add(queue_mobj)

        self.play(
            Create(creators_group),
            Create(queues_group),
            Create(arrows_group),
            Write(creator_mobj),
            Write(queue_mobj),
        )
        self.wait()

        scheduler_queue_mobj = Rectangle(
            width=0.8 * N_CPUS * COL_SPACE, height=0.2 * config.frame_height
        ).next_to(queues_group, DOWN, MED_LARGE_BUFF)
        scheduler_queue_mobj.set_fill(GREY, 0.2)

        queues_to_scheduler_arrows_group = VGroup()
        for queue in queues_group.submobjects:
            start = queue.get_center() + queue.height * DOWN / 2
            end = start + (scheduler_queue_mobj.get_top() - queues_group.get_bottom())
            arrow = Arrow(start, end, buff=0)
            queues_to_scheduler_arrows_group.add(arrow)

        scheduler_queue_text_mobj = (
            (
                Text("Scheduler\n   Queue")
                .scale(text_scale)
                .set_fill(text_color, opacity=1)
            )
            .move_to(get_center_margin())
            .shift(scheduler_queue_mobj.get_center() * UP)
        )
        margin_texts_group.add(scheduler_queue_text_mobj)

        self.play(
            Create(scheduler_queue_mobj),
            Create(queues_to_scheduler_arrows_group),
            Write(scheduler_queue_text_mobj),
        )
        self.wait()

        workers_group = VGroup()
        scheduler_to_workers_arrows_group = VGroup()
        for cpu_idx in range(N_CPUS):
            curr_cpu_mobj = deepcopy(cpu_mobj)
            curr_cpu_mobj.move_to(get_center_col(cpu_idx))
            curr_cpu_mobj.shift(
                (scheduler_queue_mobj.height + MED_SMALL_BUFF + curr_cpu_mobj.height)
                * DOWN
            )
            workers_group.add(curr_cpu_mobj)

            arrow = Arrow(
                curr_cpu_mobj.get_center() * RIGHT
                + scheduler_queue_mobj.get_bottom() * UP,
                curr_cpu_mobj.get_center() * RIGHT + curr_cpu_mobj.get_top() * UP,
                buff=0,
            )
            scheduler_to_workers_arrows_group.add(arrow)

        worker_mobj = (
            (Text(" Worker\nThreads").scale(text_scale).set_fill(text_color, opacity=1))
            .move_to(get_center_margin())
            .shift(workers_group.get_center() * UP)
        )
        margin_texts_group.add(worker_mobj)

        self.play(
            Create(workers_group),
            Create(scheduler_to_workers_arrows_group),
            Write(worker_mobj),
        )
        self.wait()

        lock_creator_queues_mobj = VGroup()
        for cpu, queue in zip(creators_group, queues_group):
            height = (
                SMALL_BUFF
                + (cpu.get_top() - queue.get_center() - 0.15 * queue.height)[1]
            )
            lock_fill_mobj = RoundedRectangle(
                width=1.25 * queue.width, height=height, color=RED
            )
            lock_fill_mobj.set_fill(RED, opacity=0.1)
            lock_fill_mobj.move_to(
                cpu.get_center() * RIGHT
                + (cpu.get_top() + SMALL_BUFF - lock_fill_mobj.height / 2) * UP
            )

            lock_mobj = get_lock_mobj(scale=0.15)
            lock_mobj.next_to(
                queue.get_right() * RIGHT + queue.get_top() * UP,
                LEFT + DOWN,
                SMALL_BUFF,
            )

            producer_mobj = Text("Producer").scale(text_scale).set_fill(RED, 1)
            producer_mobj.rotate(PI / 2)
            producer_mobj.next_to(lock_fill_mobj, LEFT, SMALL_BUFF)

            lock_creator_queues_mobj.add(
                VGroup(lock_fill_mobj, lock_mobj, producer_mobj)
            )

        height = (
            SMALL_BUFF
            + (
                queue.get_center()
                - scheduler_queue_mobj.get_bottom()
                - 0.15 * queue.height
            )[1]
        )
        lock_fill_scheduler_mobj = RoundedRectangle(
            width=1.1 * scheduler_queue_mobj.width, height=height, color=RED
        )
        lock_fill_scheduler_mobj.set_fill(RED, 0.1)
        lock_fill_scheduler_mobj.move_to(
            scheduler_queue_mobj.get_center()
            + (
                SMALL_BUFF
                + scheduler_queue_mobj.height / 2
                - lock_fill_scheduler_mobj.height / 2
            )
            * DOWN
        )

        consummer_mobj = (
            Text("Consumer")
            .scale(text_scale)
            .set_fill(RED, 1)
            .rotate(PI / 2)
            .next_to(lock_fill_scheduler_mobj, LEFT, SMALL_BUFF)
        )

        lock_mobj = get_lock_mobj(scale=0.15)
        lock_mobj.next_to(
            lock_fill_scheduler_mobj.get_left() * RIGHT
            + lock_fill_scheduler_mobj.get_top() * UP,
            DOWN + RIGHT,
            MED_SMALL_BUFF,
        )

        lock_scheduler_mobj = VGroup(
            lock_fill_scheduler_mobj, consummer_mobj, lock_mobj
        )

        self.play(Create(lock_creator_queues_mobj), Create(lock_scheduler_mobj))
        self.wait()

        self.play(
            *list(
                map(
                    Uncreate,
                    [
                        margin_texts_group,
                        creators_group,
                        lock_scheduler_mobj,
                        lock_creator_queues_mobj,
                        scheduler_queue_mobj,
                        workers_group,
                        queues_group,
                        arrows_group,
                        queues_to_scheduler_arrows_group,
                        scheduler_to_workers_arrows_group,
                    ],
                )
            )
        )
        self.wait()


class ButHowWorkers(Scene):
    def construct(self):
        rect_text = Rectangle(
            width=0.75 * config.frame_width, height=0.75 * config.frame_height
        )
        but_how = Text("But how", size=1.5).next_to(
            rect_text.get_left() * RIGHT + rect_text.get_top() * UP,
            DOWN + RIGHT,
            SMALL_BUFF,
        )
        workers_thread = Text("worker threads", size=1.5, color=BLUE).move_to(
            rect_text.get_center()
        )

        receive_work = Text("receive work?", size=1.5).next_to(
            rect_text.get_right() * RIGHT + rect_text.get_bottom() * UP,
            UP + LEFT,
            SMALL_BUFF,
        )

        but_how_title = VGroup(but_how, workers_thread, receive_work)

        cpu_mobj = get_cpu_mobj(0.75).next_to(
            rect_text.get_top() * UP + rect_text.get_right() * RIGHT, DOWN + LEFT, 0
        )
        interrogation_mobj = Text("?").next_to(
            cpu_mobj.get_top() * UP + cpu_mobj.get_right() * RIGHT,
            UP + RIGHT,
            -SMALL_BUFF,
        )
        interrogation_group = VGroup(
            *[
                deepcopy(interrogation_mobj).shift(idx * 0.2 * (RIGHT + UP))
                for idx in range(3)
            ]
        )

        # self.play(*[Write(mobj) for mobj in but_how_title.submobjects])
        self.play(Write(but_how_title))
        self.play(FadeIn(cpu_mobj), Write(interrogation_group), run_time=2)
        self.wait()


class WaitingQueue:
    def __init__(self, available_places, length, color=WHITE, title=None):
        self._available_places = available_places
        self._hspace = length / available_places
        self._queue = Rectangle(width=length, height=self._hspace, color=color)
        self._vlines = VGroup(
            *[
                Line(self._queue.get_top(), self._queue.get_bottom()).move_to(
                    self._queue.get_left() + idx * self._hspace * RIGHT
                )
                for idx in range(1, available_places)
            ]
        )
        self._values = VGroup(
            *[
                Integer(-1)
                .move_to(self._queue.get_left() + RIGHT * self._hspace / 2)
                .shift(idx * self._hspace * RIGHT)
                for idx in range(available_places)
            ]
        )

        self._mobj = VGroup(self._queue, self._vlines, self._values)

        # self._title = None
        # if title:
        #     self._title = Text(title)
        #     self._title.next_to(self._queue, LEFT, SMALL_BUFF)
        #     self._title.width = self._hspace
        #     self._mobj.add(self._title)

    @property
    def mobj(self):
        return self._mobj

    def get(self, idx, which="center"):
        return getattr(self[idx], f"get_{which}")

    def get_center_top(self, idx):
        return self[idx].get_center() + self._hspace * UP

    def set(self, idx, function, *args, **kwargs):
        value = self[idx]
        center = value.get_center()
        ret = getattr(value, function)(*args, **kwargs)
        value.move_to(center)
        return ret

    def __getitem__(self, key):
        return self._values.submobjects[key]

    def __setitem__(self, key, value):
        return self._values.submobjects[key]

    def __len__(self):
        return self._available_places


class DelegatinQueue:
    def __init__(
        self,
        available_places,
        length,
        color=WHITE,
        title=None,
        default_values=None,
        default_colors=None,
    ):
        self._available_places = available_places
        self._hspace = length / available_places
        self._queue = Rectangle(width=length, height=3 * self._hspace, color=color)
        self._vlines = VGroup(
            *[
                Line(self._queue.get_top(), self._queue.get_bottom()).move_to(
                    self._queue.get_left() + idx * self._hspace * RIGHT
                )
                for idx in range(1, available_places)
            ]
        )
        self._hlines = VGroup(
            *[
                Line(self._queue.get_left(), self._queue.get_right()).shift(
                    (-1) ** idx * self._hspace * UP / 2
                )
                for idx in range(2)
            ]
        )
        if default_values is None:
            default_values = np.full((3, available_places), -1, dtype=np.object_)
        if default_colors is None:
            default_colors = np.full((3, available_places), WHITE)
        self._values = VDict(
            {
                key: VGroup(
                    *[
                        Integer(default_values[hidx, idx])
                        .move_to(
                            self.get_center(hidx, idx)
                            # self._queue.get_left()
                            # + self._hspace * (UP - hidx * DOWN + RIGHT / 2)
                            # + (RIGHT) * self._hspace / 2
                        )
                        .set_fill(default_colors[hidx, idx], 1)
                        for idx in range(available_places)
                    ]
                )
                for hidx, key in enumerate(["now_serving", "result", "request"])
            }
        )

        self._mobj = VGroup(self._queue, self._vlines, self._hlines, self._values)

        # self._title = None
        # if title:
        #     self._title = Text(title)
        #     self._title.next_to(self._queue, LEFT, SMALL_BUFF)
        #     self._title.width = self._hspace
        #     self._mobj.add(self._title)

    @property
    def mobj(self):
        return self._mobj

    def get(self, idx, which="center"):
        return getattr(self[idx], f"get_{which}")

    def get_center(self, y, x):
        top_left = self._queue.get_top() * UP + self._queue.get_left() * RIGHT
        return top_left + ((y + 0.5) * DOWN + (x + 0.5) * RIGHT) * self._hspace

    def get_center_top(self, idx):
        return self[idx].get_center() + self._hspace * UP

    def set(self, key, function, *args, **kwargs):
        value = self[key]
        center = value.get_center()
        ret = getattr(value, function)(*args, **kwargs)
        value.move_to(center)
        return ret

    def __getitem__(self, key):
        key_dict, key_value = key
        return self._values[key_dict].submobjects[key_value]

    # def __setitem__(self, key, value):
    #     return self._values.submobjects[key]

    def __len__(self):
        return self._available_places


class TicketScheduler(Scene):
    def create_counter(
        self, width, height, color=BLUE, counter_text="Now serving", locked=True
    ):
        counter = VGroup()
        rect = Rectangle(width=width, height=height, color=color).set_fill(
            color, opacity=0.5
        )

        counter.add(rect)

        text = Text(counter_text, color=WHITE)
        text.width = 0.85 * rect.width
        text.next_to(rect.get_center() * RIGHT + rect.get_top() * UP, DOWN, SMALL_BUFF)
        counter.add(text)

        value = Integer(0)
        value.move_to(rect.get_center()).shift(DOWN * text.height / 2)
        counter.add(value)

        if locked:
            lock_mobj = get_lock_mobj(0.2).set_fill(WHITE, 1)
            lock_mobj.next_to(rect.get_corner(RIGHT + DOWN), LEFT + UP, SMALL_BUFF)
            counter.add(lock_mobj)

        return counter

    def create_ticket(self, num, radius=0.01, color=ORANGE):
        circle = Circle(radius=radius, color=color).set_fill(color, opacity=0.7)
        ticket = Text(f"Ticket {num}", color=WHITE)
        ticket.width = 1.8 * radius

        return VGroup(circle, ticket)

    def get_next_ticket_value(self, counter):
        dec_value = list(
            filter(lambda x: isinstance(x, DecimalNumber), counter.submobjects)
        )[0]
        return dec_value.get_value()

    def increment_counter(self, counter, value=1):
        dec_value = list(
            filter(lambda x: isinstance(x, DecimalNumber), counter.submobjects)
        )[0]
        dec_value.increment_value(value)

    def construct(self):
        _TOP = config.frame_height / 2 * UP
        _BOTTOM = -_TOP
        _RIGHT = config.frame_width / 2 * RIGHT
        _LEFT = -_RIGHT

        N_CPUS = 2
        H_SPACE = config.frame_width / 8
        MARGIN = config.frame_width / 5
        USABLE_WIDTH = config.frame_width - MARGIN
        COL_SPACE = (USABLE_WIDTH) / N_CPUS

        CPU_SIZE = 0.4
        BUBBLE_TEXT_SIZE = 0.4

        info = np.array([dict() for _ in range(N_CPUS)])

        V_LINES = VGroup(
            Line(
                config.top + config.frame_width * LEFT / 2 + (MARGIN) * RIGHT,
                config.bottom + config.frame_width * LEFT / 2 + (MARGIN) * RIGHT,
            )
        )

        for _ in range(N_CPUS):
            new_line = deepcopy(V_LINES.submobjects[-1])
            V_LINES.add(new_line.shift(COL_SPACE * RIGHT))

        def get_center_col(idx):
            return VGroup(
                V_LINES.submobjects[idx], V_LINES.submobjects[idx + 1]
            ).get_center()

        def get_center_margin():
            return VGroup(
                Line(_TOP + _LEFT, _BOTTOM + _LEFT), V_LINES.submobjects[0]
            ).get_center()

        cpu_mobj = get_cpu_mobj(CPU_SIZE)
        imready_mobj = Text("I'm ready!").scale(BUBBLE_TEXT_SIZE)

        ready_cpu_group = VGroup()
        ready_text_group = VGroup()
        for cpu_idx in range(N_CPUS):
            curr_cpu_mobj = get_cpu_mobj(CPU_SIZE, name=1 + cpu_idx * 8)
            curr_cpu_mobj.move_to(get_center_col(cpu_idx))
            curr_cpu_mobj.shift(_TOP + (MED_SMALL_BUFF + curr_cpu_mobj.height) * DOWN)
            ready_cpu_group.add(curr_cpu_mobj)

            ready_text_group.add(
                deepcopy(imready_mobj).next_to(curr_cpu_mobj, RIGHT + UP, SMALL_BUFF)
            )

        ready_cpu_zone = (
            RoundedRectangle(
                width=0.90 * USABLE_WIDTH, height=config.frame_height / 3.5, color=GREY
            )
            .set_fill(GREY, opacity=0.1)
            .next_to(
                _TOP + (_LEFT + MARGIN * RIGHT + _RIGHT) / 2,
                DOWN,
                SMALL_BUFF,
            )
        )

        ready_cpu_zone_text = (
            Text(" Ready\nthreads")
            .scale(0.5)
            .next_to(ready_cpu_zone, LEFT, 0)
            .shift(MARGIN * LEFT / 2)
        )

        computing_zone = deepcopy(ready_cpu_zone)
        computing_zone.set_fill(RED, 0.05)
        computing_zone.color = RED
        computing_zone.move_to(np.array([1, -1, 1]) * ready_cpu_zone.get_center())

        computing_zone_text = (
            Text("Locked\nthreads")
            .scale(0.5)
            .next_to(computing_zone, LEFT, 0)
            .shift(MARGIN * LEFT / 2)
        )

        now_serving_mobj = self.create_counter(
            0.8 * MARGIN, 0.5 * MARGIN, BLUE, counter_text="Now serving"
        )
        self.increment_counter(now_serving_mobj, 4)

        next_ticket_mobj = self.create_counter(
            0.8 * MARGIN, 0.5 * MARGIN, ORANGE, counter_text="Next ticket"
        ).next_to(now_serving_mobj, DOWN, MED_SMALL_BUFF)
        self.increment_counter(next_ticket_mobj, 5)

        VGroup(now_serving_mobj, next_ticket_mobj).move_to(_LEFT + MARGIN * RIGHT / 2)

        computing_cpu = get_cpu_mobj(CPU_SIZE, name=7)
        computing_cpu.move_to(computing_zone)

        ivethelock = (
            Text("I have the lock!")
            .scale(BUBBLE_TEXT_SIZE)
            .next_to(
                computing_cpu,
                UP + RIGHT,
                SMALL_BUFF,
            )
        )

        self.play(
            FadeIn(ready_cpu_zone),
            Write(ready_cpu_zone_text),
            FadeIn(computing_zone),
            Write(computing_zone_text),
            Create(now_serving_mobj),
            Create(next_ticket_mobj),
            Create(computing_cpu),
        )
        self.wait()
        self.play(Write(ivethelock))
        self.wait()

        tickets_group = VGroup()
        for idx, (cpu, imready) in enumerate(
            zip(ready_cpu_group.submobjects, ready_text_group)
        ):
            ticket = self.create_ticket(self.get_next_ticket_value(next_ticket_mobj))
            info[idx]["cpu"] = cpu
            info[idx]["ticket"] = ticket
            info[idx]["imready"] = imready
            self.play(
                Create(cpu),
                Write(imready),
            )
            self.wait()
            self.play(
                CounterGiveTicket(next_ticket_mobj, ticket, cpu),
                IncrementCounter(next_ticket_mobj),
            )
            self.wait()
            tickets_group.add(ticket)

        eyes_cpu_group = VGroup()
        todo = []
        for idx, (cpu, imready) in enumerate(
            zip(ready_cpu_group.submobjects, ready_text_group)
        ):
            eyes_cpu = add_eyes_on_cpu(cpu)
            info[idx]["eyes_cpu"] = eyes_cpu
            eyes_cpu_group.add(eyes_cpu)
            todo += [FadeOut(cpu), FadeIn(eyes_cpu), imready.animate.set_fill(RED, 1)]

        self.play(*todo)
        self.wait()

        self.play(
            FadeOut(eyes_cpu_group),
            FadeIn(ready_cpu_group),
            ready_text_group.animate.set_fill(WHITE, 1),
        )
        self.wait()

        _height_available = (
            ready_cpu_zone.get_bottom() - computing_zone.get_top() - 2 * MED_LARGE_BUFF
        )[1]
        _length_queue = 5 * _height_available / 3
        waiter_queue = WaitingQueue(5, _length_queue)
        waiter_queue.mobj.next_to(ready_cpu_zone, DOWN, MED_LARGE_BUFF)
        waiter_queue.set(4, "set_value", 4)
        for idx in range(len(waiter_queue) - 1):
            waiter_queue.set(idx, "set_value", idx)
            waiter_queue.set(idx, "set_fill", GREY, 1)

        local_now_serving_text = Text("Local\nNow\nServing")
        local_now_serving_text.width = waiter_queue._hspace
        local_now_serving_text.next_to(waiter_queue.mobj, RIGHT, SMALL_BUFF)

        self.play(Create(waiter_queue.mobj), Write(local_now_serving_text))
        self.wait()

        down_cpus_group = VGroup()
        for idx in range(N_CPUS):
            direction = "right" if idx < N_CPUS / 2 else "left"
            cpu = ready_cpu_group.submobjects[idx]
            eyes_cpu = add_eyes_on_cpu(cpu, which="down", direction=direction)
            down_cpus_group.add(eyes_cpu)

            self.play(
                Circumscribe(waiter_queue[idx]),
                Circumscribe(ready_cpu_group.submobjects[idx]),
                FadeOut(cpu),
                FadeIn(eyes_cpu),
            )

        self.wait()

        default_values = np.full((3, 5), -1, dtype=np.int32)
        default_values[0, :] = np.arange(5)
        default_colors = np.c_[np.full((3, 4), GREY), np.full((3, 1), WHITE)]
        delegation_queue = DelegatinQueue(
            5,
            _length_queue,
            default_values=default_values,
            default_colors=default_colors,
        )
        delegation_queue.mobj.next_to(ready_cpu_zone, DOWN, MED_LARGE_BUFF)

        result_text = (
            Text("Results")
            .move_to(local_now_serving_text)
            .shift(delegation_queue._hspace * DOWN)
        )
        result_text.width = delegation_queue._hspace

        request_text = (
            Text("Requests").move_to(result_text).shift(delegation_queue._hspace * DOWN)
        )
        request_text.width = delegation_queue._hspace

        delegation_text = VGroup(result_text, request_text)

        self.play(
            Uncreate(waiter_queue.mobj),
        )

        self.play(
            Write(delegation_text),
            Create(delegation_queue.mobj),
        )

        delegation_text += local_now_serving_text

        for idx, (cpu, value) in enumerate(zip(eyes_cpu_group, (1, 9))):
            value_to_change = delegation_queue[("request", idx)]
            self.play(
                ChangeDecimalToValue(value_to_change, value),
                Circumscribe(value_to_change),
                Circumscribe(cpu),
            )

        self.wait()

        result_to_change = delegation_queue[("result", 0)]
        self.play(
            ChangeDecimalToValue(result_to_change, 6), Circumscribe(result_to_change)
        )
        self.wait()

        self.play(ChangeDecimalToValue(result_to_change, -1))
        self.wait()

        byebye = Text("Finished, bye bye").scale(BUBBLE_TEXT_SIZE)
        byebye.next_to(computing_cpu, UP + RIGHT, SMALL_BUFF)
        byebye.generate_target()
        byebye.target.shift(10 * RIGHT)

        computing_cpu.generate_target()
        computing_cpu.target.shift(10 * RIGHT)

        self.play(FadeOut(ivethelock), FadeIn(byebye))
        self.play(
            MoveToTarget(computing_cpu),
            MoveToTarget(byebye),
        )
        self.wait()

        self.play(
            *IncrementCounter(now_serving_mobj, circumscribe=True),
            ChangeDecimalToValue(delegation_queue[("now_serving", 0)], 5),
        )
        self.wait()

        now_computing_cpu = info[0]["eyes_cpu"]

        noresult = (
            Text("No result?")
            .scale(BUBBLE_TEXT_SIZE)
            .next_to(now_computing_cpu.get_corner(UP + RIGHT), UP + RIGHT, SMALL_BUFF)
        )

        myturnthen = (
            Text("My turn then...")
            .scale(BUBBLE_TEXT_SIZE)
            .next_to(now_computing_cpu.get_corner(UP + RIGHT), UP + RIGHT, SMALL_BUFF)
        )

        now_computing_cpu.generate_target()
        now_computing_cpu.target.move_to(computing_zone)

        self.play(Unwrite(info[0]["imready"]))
        self.play(Write(noresult))
        self.play(Unwrite(noresult))
        self.play(Write(myturnthen))

        # self.play(
        #     Unwrite(myturnthen),
        #     Uncreate(info[0]["ticket"]),
        #     MoveToTarget(now_computing_cpu),
        # )
        self.wait()


class ThanksForWatching(Scene):
    def construct(self):
        frame = Rectangle(
            width=0.85 * config.frame_width, height=0.8 * config.frame_height
        )

        cpu_mobj = get_cpu_mobj(1.5)
        cpu_mobj = add_eyes_on_cpu(cpu_mobj, "happy")

        thanks = Text(
            "Thanks for watching!", t2w={"world": BOLD}, gradient=(WHITE, BLUE)
        ).next_to(cpu_mobj, UP, MED_LARGE_BUFF)

        self.play(Create(cpu_mobj), Write(thanks))

        link = (
            Text("https://github.com/RomainGrx/LINGI2355-Exam-video", color=BLUE)
            .scale(0.45)
            .next_to(cpu_mobj, DOWN, MED_LARGE_BUFF)
        )
        self.play(Write(link))
        self.wait()
