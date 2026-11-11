from drafter import *
from dataclasses import dataclass
"""from bakery import assert_equal"""
@dataclass
class ConcretePad:
    name: str
    length: float
    width: float
    thickness: float
    volume: float
@dataclass
class State:
    pad_name: str
    length: float
    width: float
    thickness: float
    unit: str
    include_waste: bool
    volume: float
    status: str
    saved_pads: list[ConcretePad]
def calculate_volume(length: float, width: float,
                     thickness: float, unit: str,
                     include_waste: bool) -> float:
    """Calculate the amount of concrete needed in cubic feet."""
    if unit == "inches":
        length = length / 12
        width = width / 12
        thickness = thickness / 12
    volume = length * width * thickness
    if include_waste:
        volume = volume * 1.10
    return volume
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Concrete Pad Calculator"),
        "This website calculates how much concrete you need for a pad.",
        Button("Open Calculator", "calculator"),
        Button("Saved Pads", "saved_pads"),
        Button("Materials Information", "materials"),
        Button("About", "about")])
@route
def calculator(state: State) -> Page:
    return Page(state, [
        Header("Concrete Calculator"),
        "Enter the measurements of your concrete pad.",
        "Pad Name:",
        TextBox("pad_name", state.pad_name),
        "Length:",
        TextBox("length", state.length),
        "Width:",
        TextBox("width", state.width),
        "Thickness:",
        TextBox("thickness", state.thickness),
        "Measurement Unit:",
        SelectBox("unit", ["feet", "inches"], state.unit),
        "Add 10% extra concrete:",
        CheckBox("include_waste", state.include_waste),
        Button("Calculate", "calculate"),
        Button("Home", "index")])
@route
def calculate(state: State, pad_name: str, length: float,
              width: float, thickness: float, unit: str,
              include_waste: bool) -> Page:
    state.pad_name = pad_name
    state.length = length
    state.width = width
    state.thickness = thickness
    state.unit = unit
    state.include_waste = include_waste
    if pad_name == "":
        state.status = "Please enter a pad name."
        return calculator(state)
    if length <= 0 or width <= 0 or thickness <= 0:
        state.status = "All measurements must be greater than zero."
        return calculator(state)
    state.volume = calculate_volume(
        length, width, thickness, unit, include_waste)
    state.status = "Your concrete amount was calculated!"
    return results(state)
@route
def results(state: State) -> Page:
    return Page(state, [
        Header("Calculation Results"),
        state.status,
        "Pad Name: " + state.pad_name,
        "Concrete Needed: " + str(round(state.volume, 2)) + " cubic feet",
        "Concrete Needed: " + str(round(state.volume / 27, 2)) + " cubic yards",
        Button("Save This Pad", "save_pad"),
        Button("Calculate Again", "calculator"),
        Button("Home", "index")])
@route
def save_pad(state: State) -> Page:
    new_pad = ConcretePad(
        state.pad_name,
        state.length,
        state.width,
        state.thickness,
        state.volume)
    state.saved_pads.append(new_pad)
    state.status = "Your pad was saved."
    return saved_pads(state)
@route
def saved_pads(state: State) -> Page:
    content = [
        Header("Saved Concrete Pads"),
        state.status]
    if len(state.saved_pads) == 0:
        content.append("You have not saved any pads yet.")
    else:
        for index, pad in enumerate(state.saved_pads):
            content.append("Pad Name: " + pad.name)
            content.append("Length: " + str(pad.length))
            content.append("Width: " + str(pad.width))
            content.append("Thickness: " + str(pad.thickness))
            content.append("Concrete: " + str(round(pad.volume, 2)) + " cubic feet")
            content.append(Button("Delete Pad", "delete_pad", pad_index=index))

    content.append(Button("Calculator", "calculator"))
    content.append(Button("Home", "index"))
    return Page(state, content)
@route
def delete_pad(state: State, pad_index: int) -> Page:
    if pad_index >= 0 and pad_index < len(state.saved_pads):
        deleted_pad = state.saved_pads.pop(pad_index)
        state.status = deleted_pad.name + " was deleted."
    else:
        state.status = "That pad could not be found."
    return saved_pads(state)
@route
def materials(state: State) -> Page:
    return Page(state, [
        Header("Concrete Materials Information"),
        "Concrete is usually ordered by cubic yards.",
        "There are 27 cubic feet in one cubic yard.",
        "It is a good idea to order a little extra concrete.",
        "This calculator can add 10% extra to your calculation.",
        Button("Home", "index")])
@route
def about(state: State) -> Page:
    return Page(state, [
        Header("About This Website"),
        "This website was made for small projects",
        "It helps calculate concrete needed for construction pads.",
        "Users can calculate, save, and delete concrete pad projects.",
        Button("Home", "index")])
set_site_information(
    author="Nathaniel Sutton",
    description="A concrete calculator for construction projects.",
    sources="Drafter documentation and class materials.",
    planning="Concrete Calculation Website.")
    links = []
start_server(State("", 10, 10, 0.5, "feet", False, 0, "", []),in_debug_mode=False,framed=True)
"""
assert_equal(calculate_concrete_volume(10, 10, 0.5, "feet", False),50)
assert_equal(calculate_concrete_volume(10, 10, 0.5, "feet", True),55)
assert_equal(calculate_concrete_volume(120, 120, 6, "inches", False),50)
assert_equal(isinstance(index(test_state), Page), True)
assert_equal(isinstance(calculator(test_state), Page), True)
assert_equal(isinstance(materials(test_state), Page), True)
assert_equal(isinstance(about(test_state), Page), True)
assert_equal(test_state.volume, 50)
assert_equal(test_state.status,"Your concrete volume was calculated successfully!")
assert_equal(len(test_state.saved_pads), 1)
assert_equal(test_state.saved_pads[0].name, "Test Pad")
assert_equal(test_state.saved_pads[0].volume, 50)
assert_equal(isinstance(results(test_state), Page), True)
assert_equal(isinstance(saved_pads(test_state), Page), True)
"""
