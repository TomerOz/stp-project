"""The classes module holds the various classes of graphical or event objects
that are used by BodyMap:
- GraphicalScene: Background graphical objects - silhouettes and buttons.
- SensationsCluster
- Trial - a two-phase instructions and rating routine.
"""

from __future__ import annotations

import os
import datetime
import typing
import numpy as np
import pandas as pd
from psychopy import visual, event, core
from psychopy.visual.rect import Rect
from psychopy.visual.text import TextStim

from skimage import io, transform

# Our project modules
import params
import utils


class GraphicalScene:
    """GraphicalScene holds the visual background for the experiment, including:
        - Body images
        - Buttons (Undo / Continue)
        - Orientation labels
        - Illustations (Intensity scale, Mouse keys legend)
        - Confirmation bar and buttons
        - Instructions
    Additionally the class handles segmentation of the body images to drawable
    and non-drawable areas.
    """

    def __init__(self, win: visual.window.Window):
        self.win = win
        # Instructions slide and button for controlling instructions routine
        self.inst_img, self.inst_confirm_button = self._gen_inst_objects()
        # Images of body
        self.body_back = self._gen_body_img('back')
        self.body_front = self._gen_body_img('front')
        # Action buttons are used to control the flow of the rating routine
        # undoing an action or finishing up the rating routine
        self.button_finish = self._gen_action_button('finish_green')
        self.button_undo = self._gen_action_button('undo_button')
        self.button_show_inst = self._gen_action_button('show_inst')
        self.eraser = self._gen_action_button('eraser')
        # Illustrations
        self.intensity_scale = self._gen_intensity_bar()
        self.colors_mouse_key = self._gen_colors_mouse_key()
        self.eraser_frame = EraserFrame(
            win, self.eraser.pos, params.ERASER_FRAME_SIZE)  # self.eraser.size
        self.cursor_marker = CursorMarker(win)

        # Generate bar and buttons used during confirmation routine
        self.confirm_bar, self.button_confirm_no, self.button_confirm_yes = (
            self._gen_confirm_objects())

        # Generate drawable and non-drawable areas
        back_in, back_out = self._yield_body_map_area('back')
        front_in, front_out = self._yield_body_map_area('front')
        self.dotting_area = np.concatenate((back_in, front_in))
        self.dotting_outlines = np.concatenate((back_out, front_out))

        # Generate orientation labels, requires coordinates from outlines
        (self.front_right_label, self.front_left_label,
         self.back_right_label, self.back_left_label,
         self.bottom_left_label, self.bottom_right_label) = (
            self._gen_orientation_labels())

    def _gen_body_img(
            self, side: str, reference: bool = False) -> typing.Union[
        visual.ImageStim, typing.Tuple[np.ndarray, tuple, tuple]]:
        """A 2-use functions, pending the reference argument:
        1. Returns a visual.ImageStim object for drawing the body image.
        2. Returns array and size/position parameters for the reference image
        which is used to set the drawing and no-drawing area.

        Parameters
        ----------
        side
            For indicating the front/back body image.
        reference
            For controlling the usage of the functions (default False), see
            usage cases above.
            On False usage #1 is selected, on True usage #2 is selected.

        Returns
        -------
        Pending `reference` parameter either:
        - Visual.ImageStim - Front/Back body image.
        - a tuple of three np.ndarray - matching the image, the position on the
          screen and the size of the image (both in pixels).
        """
        # Generate the image label based on the required side
        img_lab = dict(zip(('back', 'front'), (1, 2)))[side]
        # Get the sign of horizontal offset based on required size
        img_offset_sign = (dict(zip(('front', 'back'), (-1, 1)))[side], 1)
        # Calculate position in pixels based image offset
        pos = (self.win.size * params.IMG_OFFSET * img_offset_sign).astype(int)
        # Calculate image size in pixels
        size = (self.win.size * params.IMG_SIZE).astype(int)

        # Flip upside down as scikit-image assumes of the first pixel on y as
        # located in the bottom, while PsychoPy assumes it is located in
        # the top.
        img_ar = np.flipud(
            io.imread('./input/graphics/BodyMap-0{}{}.png'.format(
                img_lab, {False: '', True: ' - Reference'}[reference])))
        # You need to flip the size specification as resize is expecting the
        # YX size of the output
        img_ar = transform.resize(img_ar, size[::-1])
        # In case you need an array of coordinates (outlines and shape)
        if reference:
            return img_ar, pos, size
        # in case you need the body image for drawing
        return visual.ImageStim(
            win=self.win, pos=pos, image=img_ar, size=size, units='pix',
            name='{}{}_img'.format(
                side, {False: '', True: '_reference'}[reference]))

    def _gen_action_button(self, img_lab) -> visual.ImageStim:
        """A helper function to produce Undo/Finish/Show-instructions buttons.
        """
        # Pending the label of the button set the sign of the horizontal offset
        x_img_offset_sign = {
            'eraser': -1, 'undo_button': -1 + params.ACTION_BUTTON_SIZE[0] * 2.5
        }.get(img_lab, 1)
        y_img_offset_sign = {'show_inst': 1}.get(img_lab, -1)
        img_offset_sign = np.array([x_img_offset_sign, y_img_offset_sign])

        return visual.ImageStim(
            win=self.win, units='pix', pos=self.win.size
                                           * params.ACTION_BUTTON_OFFSET * img_offset_sign
                                           - (
                                                   params.ACTION_BUTTON_SIZE * self.win.size * img_offset_sign),
            image=f"./input/graphics/buttons/{img_lab}.png",
            size=self.win.size * params.ACTION_BUTTON_SIZE)

    def _gen_confirm_objects(self) -> typing.Tuple[
        visual.ImageStim, visual.ImageStim, visual.ImageStim]:
        """Draw the confirmation bar and two matching Yes/No buttons.
        """
        confirm_bar = visual.ImageStim(
            win=self.win, pos=params.CONFIRM_BAR_POS * self.win.size,
            size=params.CONFIRM_BAR_SIZE * self.win.size, units='pix')
        confirm_button_no = visual.ImageStim(
            win=self.win, units='pix',
            pos=np.array(
                [-1, 1]) * self.win.size * params.CONFIRM_BAR_BUTTON_POS,
            size=self.win.size * params.CONFIRM_BAR_BUTTON_SIZE,
            image='./input/graphics/buttons/no.png')
        confirm_button_yes = visual.ImageStim(
            win=self.win, units='pix',
            pos=self.win.size * params.CONFIRM_BAR_BUTTON_POS,
            size=self.win.size * params.CONFIRM_BAR_BUTTON_SIZE,
            image='./input/graphics/buttons/yes.png')

        return confirm_bar, confirm_button_no, confirm_button_yes

    def _gen_inst_objects(self) -> typing.Tuple[visual.ImageStim,
                                                visual.ImageStim,
                                                visual.ImageStim]:
        """Draw the instructions slide and matching confirmation button.
        """
        inst_img = visual.ImageStim(
            win=self.win, size=self.win.size, units='pix')
        inst_confirm_button = Rect(
            win=self.win, units='pix',
            size=self.win.size * params.INST_ACCEPT_BUTTON_SIZE,
            lineColor=None)
        return inst_img, inst_confirm_button

    def _gen_orientation_labels(self) -> typing.Tuple[visual.ImageStim,
                                                      visual.ImageStim,
                                                      visual.ImageStim,
                                                      visual.ImageStim,
                                                      visual.ImageStim]:
        """Draws and returns orientation labels, with position depending on
        outlines of body image and spacing depending on the font size.
        """
        # To orient the קדימה/אחורה labels at the bottom of the images
        lowest_y = self.dotting_outlines[:, 1].min()
        # To orient the right-hand 'R' label to the right of the 'back' image
        rightmost_x = self.dotting_outlines[:, 0].max()
        # The matching 'y' value
        rightmost_y = self.dotting_outlines[
            np.argmax(self.dotting_outlines[:, 0] == rightmost_x), 1]
        # To orient the left-hand 'R' label to the left of the 'front' image
        leftmost_x = self.dotting_outlines[:, 0].min()
        # The matching 'y' value
        leftmost_y = self.dotting_outlines[
            np.argmax(self.dotting_outlines[:, 0] == leftmost_x), 1]
        # Controlling height of letters, wrap length and spacing
        height = params.TEXT_LABELS_SIZE * self.win.size[1]
        # center_label
        front_right_label = TextStim(
            win=self.win, height=height,
            units='pix', text='ימין', languageStyle='RTL', color='black',
            alignHoriz='left',
            pos=[float(
                rightmost_x + leftmost_x) / 2 + 1.5 * params.TEXT_LABELS_SIZE *
                 self.win.size[0],
                 rightmost_y],
            wrapWidth=height)
        # center_right_label
        front_left_label = TextStim(
            win=self.win, height=height,
            units='pix',
            pos=[rightmost_x + 0.5 * params.TEXT_LABELS_SIZE * self.win.size[0],
                 rightmost_y],
            text='שמאל', languageStyle='RTL', alignHoriz='left',
            color='black', wrapWidth=height)
        # center_left_label
        back_left_label = TextStim(
            win=self.win, height=height,
            units='pix',
            pos=[leftmost_x - 1.5 * params.TEXT_LABELS_SIZE * self.win.size[0],
                 leftmost_y],
            text='שמאל', languageStyle='RTL', color='black', wrapWidth=height)
        # new - back_right
        back_right_label = TextStim(
            win=self.win, height=height,
            units='pix',
            pos=[float(
                rightmost_x + leftmost_x) / 2 - 2 * params.TEXT_LABELS_SIZE *
                 self.win.size[0],
                 rightmost_y],
            text='ימין', languageStyle='RTL', color='black', wrapWidth=height)

        bottom_left_label = TextStim(
            win=self.win, height=height,
            units='pix', alignHoriz='center',
            pos=[(-self.win.size[0] * params.IMG_OFFSET[0]) - 12,
                 lowest_y - height],
            text='אחורה', languageStyle='RTL', color='black',
            wrapWidth=height)
        bottom_right_label = TextStim(
            win=self.win, height=height,
            units='pix', alignHoriz='center',
            pos=[(self.win.size[0] * params.IMG_OFFSET[0]) - 12,
                 lowest_y - height],
            text='קדימה', languageStyle='RTL',
            color='black', wrapWidth=height)

        return (
            front_right_label, front_left_label, back_right_label,
            back_left_label,
            bottom_left_label, bottom_right_label)

    def _gen_intensity_bar(self) -> visual.ImageStim:
        """Draw the illustration image of sensation intensity.
        """
        return visual.ImageStim(
            win=self.win, units='pix',
            image='input/graphics/buttons/intensity_scale.png',
            pos=self.win.size * params.INTENSITY_SCALE_POS,
            size=self.win.size * params.INTENSITY_SCALE_SIZE)

    def _gen_colors_mouse_key(self) -> visual.ImageStim:
        """Draw the illustration image of a mouse with colored keys.
        """
        return visual.ImageStim(
            win=self.win, units='pix',
            image='input/graphics/buttons/colors_mouse_key.png',
            pos=self.win.size * params.COLORS_MOUSE_KEY_POS,
            size=self.win.size * params.COLORS_MOUSE_KEY_SIZE)

    def _yield_body_map_area(self, side: str
                             ) -> typing.Tuple[np.ndarray, np.ndarray]:
        """Convenience function for getting parameters (pixels, position, size)
        of a body image, and passes it for segmentation of body image into shape
        and outlines.

        Parameters
        ----------
        side
            indicating the side of the body that should be segmented.

        Returns
        -------
        shape
            a np.ndarray of xy coordinates matching the area inside the body
            image outlines.
        outlines
            a np.ndarray of xy coordinates matching the body image outlines.
        """
        img_ar, img_pos, img_size = self._gen_body_img(side, reference=True)
        shape, outlines = utils.segment_areas(img_ar, img_pos, img_size)

        return shape, outlines

    def draw_confirmation_routine(self):
        """A convenience function for drawing a confirmation bar and buttons."""
        [go.draw() for go in [self.body_back, self.body_front,
                              self.confirm_bar, self.button_confirm_no,
                              self.button_confirm_yes]]

    def draw_instructions_routine(self):
        """A convenience function for drawing instructions and an invisible
        button for recording mouse presses."""
        [go.draw() for go in [self.inst_img, self.inst_confirm_button]]

    def draw_rating_routine(self, phase):
        """A convenience function for drawing body images and buttons or
         instructions shown during rating part."""
        [go.draw() for go in
         [self.body_back, self.body_front,
          self.intensity_scale,
          self.front_right_label, self.front_left_label,
          self.back_right_label, self.back_left_label,
          self.bottom_left_label, self.bottom_right_label]]
        if phase:  # i.e. - if phase == 1 (the second phase)
            self.colors_mouse_key.draw()

    def draw_buttons(self):
        """Utility to control the order of drawing, in order to avoid drawing
        the buttons on top of other objects when relevant."""
        self.button_finish.draw()
        self.eraser.draw()
        self.eraser_frame.draw()
        self.button_show_inst.draw()
        if params.ENABLE_UNDO:
            self.button_undo.draw()

    def draw_cursor(self):
        """Utility to control the order of drawing, in order to avoid drawing
         the cursor on top of sensations."""
        self.cursor_marker.draw()


class EraserFrame(Rect):

    def __init__(self, win, pos, size):
        super().__init__(
            win=win, pos=pos, size=params.ERASER_FRAME_SIZE, fillColor=None,
            lineColor=params.ERASER_FRAME_ON_COLOR, units='pix', lineWidth=5)

    def update(self, eraser_status):
        self.setLineColor(
            [params.ERASER_FRAME_ON_COLOR, params.ERASER_FRAME_OFF_COLOR][
                eraser_status])


class CursorMarker(TextStim):
    """
    Utility to easily switch between cursor modes, given eraser status.
    """

    def __init__(self, win):
        super().__init__(
            win=win, height=params.CURSOR_MARKER_HEIGHT, units='pix',
            text='O', color=params.ERASER_OFF_COLOR, wrapWidth=1)

    def update(self, eraser_status):
        """Switchs shape and color of cursor given eraser status (e.g.,
        a black `o` when the eraser is not used).

        Parameters
        ----------
        eraser_status: bool
            Signals whether the eraser activation button was clicked on (True)
            or off (False).

        Returns
        -------
        None.
        """
        self.setColor(
            [params.ERASER_OFF_COLOR, params.ERASER_ON_COLOR][eraser_status])
        self.setText(['O', 'X'][eraser_status])

    def update_on_frame(self, pos):
        """Used to track the mouse and ensure that the next window flip would
        include the updated location.

        Parameters
        ----------
        pos: tuple
            XY coordinates of the cursor in pixels.

        Returns
        -------
        None
        """
        self.setPos(pos)
        # win.setMouseVisible(False)
        self.draw()


class SensationsCluster:
    """SensationsCluster stores the drawn sensations and offers control in terms
        of:
        - Generation or deletion
        - Coloring or de-coloring of circumference
        - Modifying intensity of a drawn sensation
    """

    def __init__(self, win: visual.window.Window):
        # To draw the sensations in
        self.win = win
        # To store information on sensations and their graphical objects
        self.sensations = pd.DataFrame(columns=(
            'time', 'frame', 'x', 'y', 'intensity', 'tone',
            'object'))

    def _get_sensation_params(self, pos):
        """Convenience function to get current intensity and tone of an existing
         sensation."""
        return self.sensations.loc[self.get_idx_by_pos(pos),
                                   ['intensity', 'tone', 'time']]

    def gen_sensation(self, pos: tuple,
                      time: typing.Union[float, None],
                      frame: typing.Union[int, None],
                      undo: bool = False):
        """A 2-use function used to generate and delete sensations.

        Parameters
        ---------
        pos
            xy coordinates of the possible new sensation (in pixels). Used to
            either generate a new sensation or track an existing sensation that
            should be deleted (pending `undo` parameter).
        time
            The time (in secs.ms) in which the sensation was drawn. None for
            `undo` cases.
        frame
            The window frame number in which the sensation was drawn. None for
            `undo` cases.
        undo
            A flag for indicating whether the sensation closest to the specified
            position should be undrawn.

        Returns
        -------
        None
        """
        if undo:
            # Drop the index of the to-be-removed dot, but before that grab
            # the params to update.
            sensation_params = self._get_sensation_params(pos)
            self.sensations = self.sensations[
                self.sensations.index != self.get_idx_by_pos(pos)].reset_index(
                drop=True)
            return True, sensation_params
        else:
            # If not removing an existing sensation, we create a new one.
            new_sensation = self._gen_sensation(pos)
            # And store it in the data frame of existing sensations
            self._store_sensation(new_sensation, time, frame)
            return True, self._get_sensation_params(pos)

    def draw_routine(self):
        """Draw the existing sensations during rating routine."""
        self.sensations['object'].apply(lambda x: x.draw())

    def get_active_locs(self) -> np.ndarray:
        """Handle the xy coordinates of existing locations (e.g, for testing
        whether a clicked location is inside an existing sensation).

        Parameters
        ----------
        None.

        Returns
        -------
        a 2d numpy array of the xy coordinates of all currently existing
        sensations.
        """
        return self.sensations[['x', 'y']].values

    def update_intensity(self, pos: np.ndarray, undo: bool = False):
        """Increases or decreases intensity of an existing sensation. As limited
            to values specified under params. Decreases based on the `undo`
            parameter.

            Parameters
            ----------
            pos
                The xy coordinates of the clicked location. in order to locate
                the nearest position.
            undo
                Flag to control whether the intensity increase should be
                canceled.

            Returns
            -------
            bool
                Indicates whether there was an update to one of the sensations
                (True), or no-update due to intensity being already at
                 maximum or minimum (False).
        """
        # Get an identifier of the relevant sensation through xy coordinates.
        idx = self.get_idx_by_pos(pos)
        # Pending the `undo` parameter:
        if undo:
            # If the intensity level is above the minimal level
            # it can be decreased
            if self.sensations.loc[idx, 'intensity'] > 1:
                self.sensations.loc[idx, 'intensity'] -= 1
                self.sensations.loc[idx, 'object'].setOpacity(
                    params.DOT_ALPHA_INTENSITIES[
                        self.sensations.loc[idx, 'intensity'] - 1])
                return True, self._get_sensation_params(pos)
        if not undo:
            # If the intensity level is below the maximal level
            # it can be increased
            if self.sensations.loc[idx, 'intensity'] < len(
                    params.DOT_ALPHA_INTENSITIES):
                self.sensations.loc[idx, 'intensity'] += 1
                self.sensations.loc[idx, 'object'].setOpacity(
                    params.DOT_ALPHA_INTENSITIES[
                        self.sensations.loc[idx, 'intensity'] - 1])
                return True, self._get_sensation_params(pos)

        # In case no intensity modification took place (e.g., the intensity
        # level was maximal and cannot be increased)
        return False, None

    def update_tone(self, pos: np.ndarray,
                    tone: np.ndarray,
                    undo: bool = False):
        """A 2-use function for coloring and de-coloring a sensation, pending
        the `undo` parameter. On False can modify the color of an existing
        sensation to either positive or negative tones.
        On True changes the existing sensation's tone to neutral.

        Parameters
        ----------
        pos
           The xy coordinates of the clicked location.
        tone
            A string of the color describing the hedonic tone of the
            sensation.


        Returns
        -------
        bool
            whether an update took place (True) or not (False, as the sensation
            is already colored in the same tone the user tried to switch to).
        """
        idx = self.get_idx_by_pos(pos)
        if undo:
            tone = params.DOT_COLOR
        if undo or self.sensations.loc[idx, 'tone'] != tone:
            self.sensations.loc[idx, 'tone'] = tone
            self.sensations.loc[idx, 'object'].setLineColor(tone)
            return True, self._get_sensation_params(pos)
        return False, None

    def get_idx_by_pos(self, pos):
        """Helper function to identify the relevant sensation based on xy
        coordinates. Basically Pythagoras - a distance between two points.

        Parameters
        ----------
        pos
            The xy coordinates of the clicked location.
        Returns
        -------
        idx
            The index of the existing sensation nearest the supplied position.
        """
        return np.argmin(np.sum(np.power(
            self.get_active_locs() - pos, 2), 1))

    def _gen_sensation(self,
                       pos: typing.Union[
                           list, tuple, np.ndarray]) -> visual.Circle:
        """
        Generate and return a visual.Circle object, as a new sensation in the
        cluster.

        Parameters
        ----------
        pos
            The xy coordinates in pixels matching the clicked position.

        Returns
        -------
        sensation
            A visual.Circle object taking parameters from the supplied xy
            position and from parameters defined in the param module.
        """
        sensation = visual.Circle(
            win=self.win,
            units='pix',
            fillColor=params.DOT_COLOR,
            opacity=params.DOT_ALPHA,
            pos=pos,
            lineWidth=params.DOT_LINE_WIDTH,
            lineColor=params.DOT_COLOR,
            radius=params.DOT_RADIUS,
        )
        return sensation

    def _store_sensation(self, sensation: visual.Circle,
                         time: float, frame: int):
        """
        Convenience function to store the sensation in the

        Parameters
        ----------
        sensation
            A sensation returned by _gen_sensation to be stored.
        time
            Timestamp of creation.
        frame
            Window frame of creation.

        Returns
        -------
        None.
        """
        # Setting with enlargement (i.e., appending the next line).
        self.sensations.loc[self.sensations.shape[0]] = (
            time,  # 'time' - Time of drawing
            frame,  # 'frame' - Window flip of drawing
            *sensation.pos,  # ['x', 'y'] - xy_pos in pixels.
            1,  # 'intensity' Initial intensity
            sensation.lineColor,  # 'tone' - hedonic tone of sensation
            sensation  # 'object' - the object itself, used for drawing.
        )


class BodyMapTask:
    """BodyMapTask is the actual rating object. It uses the GraphicalScene
    and SensationCluster to show the current instructions, available buttons
    and drawn sensations. It handles the mouse presses of the user to draw or
    undraw sensations or advance between instruction/confirmation screens.
    Finally, it stores the log of performed actions (and saves the output).

    parameters
    ----------
    win
        A PsychoPy Graphical Window.
    scene
        A BodyMap task graphical scene object.
    cluster
        A BodyMap task SensationsCluster object.
    mouse
        A Psychopy event.Mouse object.
    additional_info
        A dictionary, any information you want stored - participant id,
        condition, population, session etc.

    returns
    -------
    a BodyMapTask object.
    """

    def __init__(self, win, scene, cluster, mouse,
                 additional_info, block):
        self.win = win
        self.scene = scene
        self.cluster = cluster
        self.mouse = mouse
        self.additional_info = additional_info
        self.actions_log = pd.DataFrame(
            columns=('frame', 'time', 'x', 'y',
                     'event_type', 'undo_action', 'intensity_result',
                     'tone_result',
                     'time_sensation_created',
                     'action_cancelled', 'phase',
                     'event_num', 'undo_trigger'))
        self.additional_info['timestamp'] = str(
            datetime.datetime.today().replace(microsecond=0)).replace(
            ' ', '_').replace(':', '-')

        self.clock = core.Clock()
        self.frameN = 0
        self.phase = 0
        self._update_graphical_objects(block)
        self.eraser_on = False

    def run_task(self, block):
        self._roll_instructions()
        self._roll_rating()
        self.phase += 1
        self._update_graphical_objects(block)
        self._roll_instructions()
        self._roll_rating()
        self.phase += 1
        if block == 'neg':
            self._update_graphical_objects(block)
            self._roll_instructions()  # slide 'end of task' Slide11
        self.end_routine()

    def _update_graphical_objects(self, block):
        """A convenience function for updating the slides/buttons accordingly
        to task phase."""
        # Position the instructions confirmation button accordingly to the
        # slide shown on each phase of the task.
        self.scene.inst_confirm_button.setPos(
            self.win.size * {2: params.INST_ACCEPT_TASK_DONE_BUTTON_POS}.get(
                self.phase, params.INST_ACCEPT_BUTTON_POS))
        # Select and set the relevant slide
        if block == 'neg':
            inst_str = "./input/graphics/instructions/Slide" \
                       f"{['4', '7', '11'][self.phase]}.JPG"
            self.scene.inst_img.setImage(inst_str)
        else:
            inst_str = "./input/graphics/instructions/Slide" \
                       f"{['4', '7'][self.phase]}.JPG"
            self.scene.inst_img.setImage(inst_str)

        # Select and set the relevant confirmation bar for ending a rating
        # routine.
        if self.phase < 2:
            inst_str = "./input/graphics/buttons/AreYouSure" \
                       f"{self.phase + 1}.png"
            self.scene.confirm_bar.setImage(inst_str)

    def _roll_instructions(self):
        """A routine to show the instructions for the current phase.
        Loops until the confirmation button has been clicked.
        Returns None"""
        while True:
            self.scene.draw_instructions_routine()
            self.win.flip()
            if self.mouse.isPressedIn(self.scene.inst_confirm_button):
                return

    def _roll_confirm(self):
        """A routine to show the confirmation routine for ending the current
        phase. Loops until either button has been clicked.

        Returns
        -------
        bool
            Indicating whether to end the current phase (True) or
            continue rating (False).
        """
        while True:
            self.scene.draw_confirmation_routine()
            self.cluster.draw_routine()
            self.win.flip()
            if self.mouse.isPressedIn(self.scene.button_confirm_no):
                return False
            elif self.mouse.isPressedIn(self.scene.button_confirm_yes):
                return True

    def _roll_rating(self):
        """Controls the flow of the rating routine. Loops until participant
        selected to end routine.
        """

        self.clock.reset()
        # Boolean set to control when to end current phase.
        finished_phase_confirmed = False
        # Boolean set to control
        self.mouse_keys_currently_down = False
        # Reset eraser status
        self.eraser_on = False
        self.scene.eraser_frame.update(self.eraser_on)
        self.scene.cursor_marker.update(self.eraser_on)

        while not finished_phase_confirmed:

            drawing_this_frame, finished_phase_confirmed = (
                self._handle_mouse_events())

            self.scene.draw_rating_routine(self.phase)
            self.cluster.draw_routine()
            self.scene.draw_cursor()
            self.scene.draw_buttons()
            self.win.flip()

            if drawing_this_frame:
                core.wait(params.WAIT_PERIOD)
            self.frameN += 1
            self.current_time = self.clock.getTime()

            if event.getKeys([params.END_EXP_KEY]):  # for debugging
                self.end_routine()
                core.quit()

    def _handle_mouse_events(self):
        """Used for the interaction of the user with the BodyMap, given mouse
        status, the following can occur:
        - Drawing of new sensations.
        - changing the intesntisy or hedonic tone of existing sensations.
        - Cancelling previous events ('Undo' button).
        - Continuing to the following phase.
        - Re-viewing the instructions for the current phase.
        """
        # By default, continue the current phase.
        finished_phase_confirmed = False
        # To control delay between frames in which drawing takes place.
        drawing_this_frame = False
        # Status of currently pressed buttons.
        mouse_buttons_down = self.mouse.getPressed()

        # store mouse position
        xy_pos = self.mouse.getPos()
        x_pos = xy_pos[0] - params.DOT_RADIUS
        y_pos = xy_pos[1]
        self.scene.cursor_marker.update_on_frame((x_pos, y_pos))

        # If only one of the mouse buttons is held down (to have certainty
        # regarding the required result of the press)
        if np.sum(
                mouse_buttons_down) == 1 and (
                params.ALLOW_CONTINUOUS_DRAWING or
                not self.mouse_keys_currently_down):
            self.mouse_keys_currently_down = True

            # Test whether the pressed pixel is inside the body images
            if utils.test_if_point_in_area(xy_pos,
                                           self.scene.dotting_area):
                # Test whether the pressed pixel is within the radius of a
                # previously drawn sensation
                if utils.test_xy_proximity(
                        xy_pos, self.cluster.get_active_locs()):
                    if self.eraser_on:
                        self._undo_action(trigger='eraser', xy_pos=xy_pos)
                    # If it is within radius distance, we may need to update
                    # the nearest sensation rather than create a new one.
                    elif not self.eraser_on:

                        if mouse_buttons_down[self.phase]:
                            # The leftmost button is 0 (matching Phase 0),
                            # the middle mouse button is 1 (matching Phase 1)
                            self._do_action('intensify', xy_pos)
                            # If phase is 1 and either the leftmost or rightmost
                            # buttons were pressed, but not both.
                        elif self.phase and (mouse_buttons_down[0] or
                                             mouse_buttons_down[2]):
                            button = np.argmax(mouse_buttons_down)
                            tone = [params.TONE_MB_LEFT, params.TONE_MB_RIGHT][
                                bool(button)]
                            self._do_action('colorize', xy_pos, tone)

                # Test whether the mouse click was in dotting area or
                # may draw on outlines and the eraser is off.
                elif self._test_clicking_on_outlines(xy_pos) and (
                        not self.eraser_on):
                    if mouse_buttons_down[self.phase]:
                        # self.actions_log.creation
                        self._do_action('generate', xy_pos)

                # Whether we should have a slight pause following the current
                # frame, as some drawing took place.
                drawing_this_frame = True

            elif visual.helpers.pointInPolygon(*xy_pos,
                                               self.scene.eraser):
                # The mouse was clicked within the 'Eraser' button, so we
                # need to turn it on
                self.eraser_on = 1 - self.eraser_on  # e.g. 0 => 1
                drawing_this_frame = True
                self.scene.eraser_frame.update(self.eraser_on)
                self.scene.cursor_marker.update(self.eraser_on)
                # The Mouse was clicked within the 'Finish current phase' button
            elif visual.helpers.pointInPolygon(*xy_pos,
                                               self.scene.button_finish):
                _currently_eraser_on = self.eraser_on
                finished_phase_confirmed = self._roll_confirm()
                # The Mouse was clicked within the 'Show instructions' button
            elif visual.helpers.pointInPolygon(*xy_pos,
                                               self.scene.button_show_inst):
                self._roll_instructions()

            elif params.ENABLE_UNDO:
                # We have undo button enabled
                if visual.helpers.pointInPolygon(*xy_pos,
                                                 self.scene.button_undo):
                    # The Mouse was clicked within the 'Undo' button
                    self._undo_action(trigger='undo_button')
                    drawing_this_frame = True

        # No key is pressed at the moment.
        elif np.sum(mouse_buttons_down) == 0:
            self.mouse_keys_currently_down = False

        return drawing_this_frame, finished_phase_confirmed

    def _test_clicking_on_outlines(self, xy_pos):
        """A Convenience function for controlling drawing on outlines.
        """
        # If drawing on outlines is permitted or
        return params.ALLOW_DRAWING_ON_LINES or (
            # If drawing on lines is not permitted and none of the
            # to-be-drawn pixels is included in the shape outlines
                not params.ALLOW_DRAWING_ON_LINES and not np.sum(
            [utils.test_if_point_in_area(i,
                                         self.scene.dotting_outlines)
             for i in utils.get_in_radius_pixels(xy_pos,
                                                 params.DOT_RADIUS)])
        )

    def _do_action(self, event_type: str, xy_pos: np.ndarray, tone=None):
        """Used for 'do-events' - when a new sensation is drawn, when intensity
        is increased or when a different tone is set for an existing sensation.

        Parameters
        ----------
        event_type
            'generate', 'intensity' or 'colorize' - destring the action that
            should be performed.
        xy_pos
            The X and Y coordinates of the clicked location, in pixels.
        tone
            A string (taken off the params file), representing the tone matching
            the hedonic tone that should be set.

        Returns
        -------
        None
        """
        if event_type == 'generate':
            should_log, sensation_params = (
                self.cluster.gen_sensation(
                    xy_pos, self.current_time, self.frameN))
        else:
            if event_type == 'intensify':
                should_log, sensation_params = self.cluster.update_intensity(
                    xy_pos)
            elif event_type == 'colorize':
                should_log, sensation_params = (
                    self.cluster.update_tone(xy_pos, tone))

            # We want to match the coordinates of the registered sensation
            # and not the click per se (which may just somewhere within
            # radius distance).
            xy_pos = _x, _y = self.cluster.sensations.loc[
                self.cluster.get_idx_by_pos(xy_pos), ['x', 'y']]

        if should_log:
            self.actions_log.loc[self.actions_log.shape[0]] = (
                self.frameN,  # 'frame'
                self.current_time,  # 'time'
                *xy_pos,  # ['x', 'y']
                event_type,  # 'event_type'
                False,  # 'undo_action'
                *sensation_params,  # ['intensity',
                # 'tone_result',
                # 'time_sensation_created']
                False,  # 'action_cancelled'
                self.phase,  # 'phase'
                self.actions_log.loc[np.invert(  # 'event_num'
                    self.actions_log['undo_action'].astype(bool))].shape[0],
                None  # undo_trigger
            )

    def _undo_action(self, trigger='undo_button', xy_pos=None):
        """Used for 'undo-events' - when the user clicks the undo button, for
        cancelling a previous event or when the 'eraser' is on.

        Parameters
        ----------
        trigger: str
            Controls whether the undo action was initiated by clicking the
            undo button or activating the eraser and clicking on a sensation.
            Optional values are 'undo_button' or 'eraser'.
            Default is 'undo_button'.
        xy_pos: tuple
            X and Y coordinates of the clicked sensation, in pixels.
            Used only when the eraser initiated the undo action.

        Returns
        -------
        None
        """

        # for the undo button we need to check whether there are any actions
        # that we can cancel, and select last `params.UNDO_NUM` do events,
        # filtering out the not cancelled events.
        if trigger == 'undo_button':
            available_last_actions = self.actions_log.loc[
                self.actions_log['undo_action'] == False].copy().reset_index(
            ).tail(params.UNDO_NUM)

            # Remove actions that were allready cancelled
            available_last_actions = available_last_actions.loc[
                (available_last_actions['action_cancelled'] == False)]

        # If there is an action available for cancelling, or we initiated the
        # undo-event using the eraser (eraser operates only on existing
        # sensations, hence there must be an existing do action that we can
        # cancel.
        if trigger == 'eraser' or not available_last_actions.empty:
            if trigger == 'undo_button':
                last_action = available_last_actions.copy().iloc[-1].drop(
                    labels=['index']).to_dict()
            if trigger == 'eraser':  # For 'eraser' events
                # Find the XY coordinates of the clicked sensation, we have
                # only approximate location and we need to select the closest
                # sensation.
                _x, _y = self.cluster.sensations.loc[
                    self.cluster.get_idx_by_pos(xy_pos), ['x', 'y']]
                # Grab the actions in the original coordinates
                # that were not yet cancelled, and then the last available one.\

                # Ugly boolean indexing below, but ensures compatibility both with pandas 0.25 and 1.03.
                last_action = self.actions_log.loc[
                    (self.actions_log['x'] == _x) &
                    (self.actions_log['y'] == _y) &
                    (self.actions_log['undo_action'] == False) &
                    (self.actions_log['action_cancelled'] == False)].iloc[
                    -1].to_dict()

            # Pending the relevant event type
            if last_action['event_type'] == 'generate':
                should_log, sensation_params = self.cluster.gen_sensation(
                    pos=[last_action['x'], last_action['y']],
                    time=None, frame=None, undo=True)
            elif last_action['event_type'] == 'intensify':
                should_log, sensation_params = self.cluster.update_intensity(
                    pos=[last_action['x'], last_action['y']],
                    undo=True)
            elif last_action['event_type'] == 'colorize':
                should_log, sensation_params = self.cluster.update_tone(
                    pos=[last_action['x'], last_action['y']],
                    tone=None, undo=True)

            if should_log:
                # Refraining from using 'Dict.update' as it changes order of
                # columns, even though it would have been more elegant.
                last_action['undo_action'] = True
                last_action['time'] = self.current_time
                last_action['frame'] = self.frameN
                last_action['phase'] = self.phase
                last_action['action_cancelled'] = True
                last_action['undo_trigger'] = trigger
                (last_action['intensity_result'],
                 last_action['tone_result'],
                 last_action['time_sensation_created']
                 ) = sensation_params

                # Now put the undo-changes back into the log
                self.actions_log.loc[self.actions_log.shape[0]] = list(
                    last_action.values())
                # And update the log that the action has been cancelled
                self.actions_log.loc[
                    (self.actions_log['event_num'] == last_action['event_num']),
                    'action_cancelled'] = True

    def end_routine(self):
        """When either the last phase is finished or when the experiment is
        terminated prematurely.
        """

        # Add the current timestamp for indicating when was the experiment
        # terminated
        self.additional_info['experiment_ended'] = str(
            datetime.datetime.today().replace(microsecond=0)).replace(
            ' ', '_').replace(':', '-')

        self.save_data()

    def save_data(self):
        """The `cluster` CSV gives an image of the drawn sensations present
        during saving, but does not include dynamic information of the changes
        made to stimuli during each phase.
        The `actions` CSV can be used for analyzing the process in time
        as it includes both do and undo events.
        """
        # Generate stub of file name
        fstub = '; '.join(
            ['{}~{}'.format(k, v) for k, v in self.additional_info.items()
             if k != 'experiment_ended']
        ) + '.csv'

        # Add the monitor resolution to the log
        self.additional_info['monitor_resolution_x'] = params.SCREEN_SIZE[0]
        self.additional_info['monitor_resolution_y'] = params.SCREEN_SIZE[1]
        # For reference
        self.additional_info['front_x_pos'] = self.scene.body_front.pos[0]
        self.additional_info['front_y_pos'] = self.scene.body_front.pos[1]
        self.additional_info['front_x_size'] = self.scene.body_front.size[0]
        self.additional_info['front_y_size'] = self.scene.body_front.size[1]
        self.additional_info['back_x_pos'] = self.scene.body_back.pos[0]
        self.additional_info['back_y_pos'] = self.scene.body_back.pos[1]
        self.additional_info['back_x_size'] = self.scene.body_back.size[0]
        self.additional_info['back_y_size'] = self.scene.body_back.size[1]

        # Merge additional info into data frames
        self.actions_log = (
            pd.merge(self.actions_log.assign(A=1),
                     pd.DataFrame(self.additional_info,
                                  index=[0]).assign(A=1), on='A').drop('A',
                                                                       1)
        )
        self.cluster.sensations = (
            pd.merge(self.cluster.sensations.assign(A=1),
                     pd.DataFrame(self.additional_info,
                                  index=[0]).assign(A=1), on='A').drop('A',
                                                                       1)
        )

        # Add one-to-one identifier between actions log and sensations log
        sensations_log_times = self.cluster.sensations['time'].values
        mapper = dict(zip(sensations_log_times,
                          range(len(sensations_log_times))))
        self.cluster.sensations['identifier'] = mapper.values()
        self.actions_log.loc[
            self.actions_log['time_sensation_created'].isin(
                sensations_log_times), 'identifier'] = (
            self.actions_log.loc[
                self.actions_log['time_sensation_created'].isin(
                    sensations_log_times), 'time_sensation_created']).map(
            mapper)

        # Add output directory in case it is missing.
        for d in ['actions', 'cluster']:
            if not os.path.exists(f'./output/{d}'):
                os.makedirs(f'./output/{d}')

        # Save the currently existing sensations
        self.cluster.sensations.drop(columns=['object', 'frame']).to_csv(
            f"./output/cluster/cluster_{fstub}",
            index=False)
        # Save a detailed log of the do and undo events that took place.
        self.actions_log.drop(columns=['frame']).to_csv(
            f"./output/actions/actions_{fstub}.csv",
            index=False)
