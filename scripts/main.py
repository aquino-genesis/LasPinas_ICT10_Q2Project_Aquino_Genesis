##########################
# DimensionReset | main.py

# primarily where I handle all of the events
# all helper functions can be used here
##########################

print("Loaded!")

# === LIBRARIES ===
import random
from js import document, window
from pyodide.ffi import create_proxy
from helper import *

# === GLOBALS ===

# lets the options cursor check what is currently selected
current_selected_span = None

# proxy - global check for c press
escape_press_proxy = None # for event cleaning

# === MAIN ===

# proxy - cursor check for viewport resizing
resize_proxy = create_proxy(update_cursor_position)
window.addEventListener("resize", resize_proxy)

# Event logic when pressing Escape in a scene
def exit_scene(event):
    global escape_press_proxy

    if event.code == "Escape":
        playSound("hideSFX")
        load_options()
        if escape_press_proxy:
            window.removeEventListener("keydown", escape_press_proxy)
            escape_press_proxy.destroy()
            escape_press_proxy = None

# Helper to load different scenes by removing their "hidden" class
# it uses the global "escape_press_proxy" so i cant frickin remove it augh
def load_scene(name):
    global escape_press_proxy

    name = str(name).lower()
    sceneContainer = document.getElementById(f"{name}Menu")

    if not sceneContainer:
        playSound("bumperEndSFX")
        return

    options_menu = document.getElementById("optionsMenu")
    all_scenes = document.querySelectorAll('div#sceneContainer div[id$="Menu"]')

    if options_menu:
        options_menu.classList.add("hidden")
        svg_container.classList.add("hidden")

    for scene in all_scenes:
        scene.classList.add("hidden")

    playSound("activationSFX")
    sceneContainer.classList.remove("animate-circle-wipe")
    sceneContainer.offsetHeight
    sceneContainer.classList.remove("hidden")
    sceneContainer.classList.add("animate-circle-wipe")

    if escape_press_proxy:
        window.removeEventListener("keydown", escape_press_proxy)
        escape_press_proxy.destroy()

    escape_press_proxy = create_proxy(exit_scene)
    window.addEventListener("keydown", escape_press_proxy)

# Event logic for when cycling through <li> in option menu with arrows or WASD
def option_select_arrow(event):
    if document.getElementById("optionsMenu").classList.contains("hidden"):
        return

    svg_container.className = ""
    global current_selected_span

    last_selected_text = document.querySelector("#optionsList li span.text-black")
    current_selected_span = document.querySelector("#optionsList > li > span")

    if last_selected_text:
        current_li = last_selected_text.closest("li")

        if event.code == "KeyW" or event.code == "ArrowUp":
            if not current_li.previousElementSibling:
                next_li = document.querySelector("#optionsList > li:last-child")
            else:
                next_li = current_li.previousElementSibling
        elif event.code == "KeyS" or event.code == "ArrowDown":
            if not current_li.nextElementSibling:
                next_li = document.querySelector("#optionsList > li")
            else:
                next_li = current_li.nextElementSibling
        elif event.code == "Space":
            load_scene(last_selected_text.innerHTML)
            return
        else:
            return

        if next_li:
            target_span = next_li.querySelector("span")
            if target_span:
                last_selected_text.classList.remove("text-black")
                current_selected_span = target_span
        else:
            current_selected_span = last_selected_text.closest("span")

    if current_selected_span:
        current_selected_span.classList.add("text-black")
        playSound("uiSliderSFX")
        update_cursor_position()

# Event logic for when cycling through skill menu with arrows or WASD
def skill_select_arrow(event):
    if document.getElementById("creatorMenu").classList.contains("hidden"):
        return

    current_selected = document.querySelector("#creatorMenu #skillsList > div")
    last_selected = document.querySelector("#creatorMenu #skillsList div.bg-white")

    if last_selected:
        if event.code == "KeyW" or event.code == "ArrowUp":
            if not last_selected.previousElementSibling:
                current_selected = document.querySelector("#creatorMenu #skillsList > div:last-child")
            else:
                current_selected = last_selected.previousElementSibling
        elif event.code == "KeyS" or event.code == "ArrowDown":
            if not last_selected.nextElementSibling:
                current_selected = document.querySelector("#creatorMenu #skillsList > div")
            else:
                current_selected = last_selected.nextElementSibling
        elif event.code == "Space" or event.code == "Enter":
            playSound("bumperEndSFX")
            return
        else:
            return

        last_selected.classList.remove("bg-white", "text-black", "shadow-[0px_-8px_0px_0px_rgba(255,0,0,1)]", "animate-shadow-grow")

    if current_selected:
        if current_selected.querySelector("span") and current_selected.querySelector("span").dataset.desc:
            document.getElementById("skillDescription").innerHTML = current_selected.querySelector("span").dataset.desc

        current_selected.classList.add("bg-white", "text-black", "shadow-[0px_-8px_0px_0px_rgba(255,0,0,1)]", "animate-shadow-grow")
        playSound("uiSliderSFX")

# Event logic for when option is clicked
def option_select_mouse(event):
    if document.getElementById("optionsMenu").classList.contains("hidden"):
        return

    svg_container.className = ""
    global current_selected_span
    last_selected_text = document.querySelector("#optionsList li span.text-black")
    clicked_item_text = event.target.closest("span")

    if not clicked_item_text:
        return

    if last_selected_text:
        if clicked_item_text == last_selected_text:
            load_scene(clicked_item_text.innerHTML)
            return

        last_selected_text.classList.remove("text-black")

    clicked_item_text.classList.add("text-black")

    current_selected_span = clicked_item_text
    playSound("uiSliderSFX")
    update_cursor_position()

# Event logic for when skill is clicked
def skill_select_mouse(event):
    if document.getElementById("creatorMenu").classList.contains("hidden"):
        return

    current_selected = event.target.closest("#skillsList > div")
    if not current_selected:
        return

    last_selected = document.querySelector("#creatorMenu #skillsList div.bg-white")

    if last_selected:
        last_selected.classList.remove("bg-white", "text-black", "shadow-[0px_-8px_0px_0px_rgba(255,0,0,1)]", "animate-shadow-grow")

    if current_selected == last_selected:
        playSound("bumperEndSFX")
        return


    if current_selected.querySelector("span") and current_selected.querySelector("span").dataset.desc:
        document.getElementById("skillDescription").innerHTML = current_selected.querySelector("span").dataset.desc

    current_selected.classList.add("bg-white", "text-black", "shadow-[0px_-8px_0px_0px_rgba(255,0,0,1)]", "animate-shadow-grow")
    playSound("uiSliderSFX")

# Event logic for exiting loading screen on any keypress
def handle_loading_exit(event):
    # < Menus >
    transition_vid = document.getElementById("transitionVid")

    loading_bg_vid = document.getElementById("loadingBgVid")
    main_bg_vid = document.getElementById("mainBgVid")

    loading_menu = document.getElementById("loadingMenu")
    options_menu = document.getElementById("optionsMenu")

    # remove prev scene here
    if loading_menu:
        loading_menu.classList.add("hidden")
        playSound("launchSFX")

    # load scene
    if options_menu:
        transition_vid.play()
        playSound("colorYourNightMUS")

        def setup_options_menu(event=None):
            loading_bg_vid.classList.add("hidden")

            list_items = document.querySelectorAll("#optionsList li")
            depth = 1

            # text has cool depth staircase type effect
            for item in list_items:
                random_offset = random.uniform(-12, -9)

                if depth == 1:
                    item.classList.add("z-3")
                elif depth == 2:
                    item.classList.add("z-2", "text-[#3bc5fc]")
                else:
                    item.classList.add("z-1", "text-[#5fccfa]")
                    depth = 0

                depth += 1

                # check for item click for cursor shi
                click_proxy = create_proxy(option_select_mouse)
                item.addEventListener("click", click_proxy)

                item.classList.add(f"-my-{(random_offset/10)*-1}", "cursor-pointer", "inline-block", "relative")
                item.style.transform = f"rotate({random_offset}deg)"

            # setup mouse events for skill here so init dont bug
            for item in document.querySelectorAll("#skillsList > div"):
                # check for SKILL click for cursor shi
                skill_click_proxy = create_proxy(skill_select_mouse)
                item.addEventListener("click", skill_click_proxy)

            options_menu.classList.remove("hidden")

        # event logic for checking transition timestamp and adding in the options
        def transition_video_time(event):
            if transition_vid.currentTime >= 1.5:
                setup_options_menu()
                transition_vid.removeEventListener("timeupdate", transition_time_proxy)
                transition_time_proxy.destroy()

        # event logic for checking if transition is done then looping the actual bg
        def transition_video_end(event):
            main_bg_vid.play()
            main_bg_vid.classList.remove("hidden")
            transition_vid.classList.add("hidden")

        # < TRANSITION PROXIES >
        # check for end
        transition_end_proxy = create_proxy(transition_video_end)
        transition_vid.addEventListener("ended", transition_end_proxy)

        # check for timestamp
        transition_time_proxy = create_proxy(transition_video_time)
        transition_vid.addEventListener("timeupdate", transition_time_proxy)

    # load proxy cleanup
    window.removeEventListener("keydown", loading_proxy)
    loading_proxy.destroy()

# < KEYPRESS PROXIES >
# keypress in options list
option_arrow_proxy = create_proxy(option_select_arrow)
window.addEventListener("keydown", option_arrow_proxy)

# keypress in creator list
skill_arrow_proxy = create_proxy(skill_select_arrow)
window.addEventListener("keydown", skill_arrow_proxy)

# keypress in loading
loading_proxy = create_proxy(handle_loading_exit)
window.addEventListener("keydown", loading_proxy)

# Event logic for when user inputs first and last name into form and submits
def club_check(event):
    # get strings without spaces
    f_raw = document.getElementById("clubFName").value.replace(" ", "")
    l_raw = document.getElementById("clubLName").value.replace(" ", "")
    
    # capitalize dem words
    f_name = f_raw.capitalize()
    l_name = l_raw.capitalize()

    # concat
    full_name = f"{f_name} {l_name}"

    # tuple that stores if first or last name is missing
    # false means it isnt missing
    missing_status = (not f_raw, not l_raw)
    
    # map missing name outcomes to tuple values
    validation_responses = {
        (True, True):   lambda: club_output("Did I spell my first name right?"),
        (True, False):  lambda: club_output("Did I spell my first name right?"),
        (False, True):  lambda: club_output("Did I spell my last name right?"),
    }

    # check for if name is a persona user
    is_valid_user = full_name in persona_users
    # ma'am persona users are what my "club" is based off
    # you should play persona 3 or persona 5 they're rly good :D
    
    def success_outcome():
        club_output("I feel like I've forged a powerful bond...")
        playSound(socialLinkNoteSFX)

    def failure_outcome():
        club_output(f'"{full_name}"... I don\'t think I spelled that correctly...')

    # map fully provided name outcomes to booleans
    user_responses = {
        True:  success_outcome,
        False: failure_outcome
    }

    # if a name is missing, use the corresponding validation_responses
    # if no name is missing, fall back to user_responses
    action = validation_responses.get(missing_status, user_responses.get(is_valid_user))
    action()

    # did this all make you happy ma'am i did allat without if statements :')
    # just let us use conditionals ma'am NO ONE likes using goofy lookups