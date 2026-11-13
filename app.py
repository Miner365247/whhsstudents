import gi,json,pyperclip,subprocess,platform
print(platform.system())
command_to_open_img={
    "Linux":"xdg-open \"%s\"",
    "Windows":"powershell -Command \"%s\"",
    "Darwin":"open \"%s\""
}
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GLib
with open('students.json') as file:
    students=json.load(file)
studentslist=[]
for student in students:
    studentslist.append(f'{student["firstName"]} {student["lastName"]}')
preloaded_student_info={}
for index in range(len(studentslist)):
    preloaded_student_info[studentslist[index]]=students[index]
studentslist.sort()
class SearchableButtonWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(400, 400)
        self.set_title("WHHS Roster")

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # 1. Create a HeaderBar
        header_bar = Adw.HeaderBar()
        content_box.append(header_bar)

        # 2. Create a horizontal box container for the center of the HeaderBar
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.add_css_class("linked")  # Glues the search entry and button together nicely

        # Create the SearchEntry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search roster...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        title_box.append(self.search_entry)

        # Create the Filter MenuButton
        filter_btn = Gtk.MenuButton()
        filter_btn.set_icon_name("open-menu-symbolic")
        filter_btn.set_tooltip_text("Filter Options")
        
        # 2. Create a custom Gtk.Popover to hold the checkboxes
        popover = Gtk.Popover()
        
        # Container inside the popover
        popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        popover_box.set_margin_start(12)
        popover_box.set_margin_end(12)
        popover_box.set_margin_top(12)
        popover_box.set_margin_bottom(12)

        # Dictionary to track the state of each filter
        self.active_filters = {
            "7": True,
            "8": True,
            "9": True,
            "10": True,
            "11": True,
            "12": True
        }

        # Create checkboxes for each multi-select option
        filter_options = [
            ("7", "7th Graders (Effies)"),
            ("8", "8th Graders (E-Flats)"),
            ("9", "9th Graders (Freshmen)"),
            ("10", "10th Graders (Sophomores)"),
            ("11", "11th Graders (Juniors)"),
            ("12", "12th Graders (Seniors)")
        ]
        self.filterlist=[]
        for key, label in filter_options:
            chk = Gtk.CheckButton(label=label)
            initial_state = self.active_filters.get(key, False)
            chk.set_active(initial_state)
            chk.connect("toggled", self.on_filter_toggled, key)
            popover_box.append(chk)
            self.filterlist.append(chk)
            
        reset_btn = Gtk.Button()
        reset_btn.set_icon_name("view-refresh-symbolic")
        reset_btn.set_tooltip_text("Reset Filters")
        reset_btn.add_css_class("destructive-action")
        reset_btn.add_css_class("pill")
        reset_btn.connect("clicked",self.reset_filters)
        popover_box.append(reset_btn)
        
        
        # Put the box into the popover, and the popover into the menu button
        popover.set_child(popover_box)
        filter_btn.set_popover(popover)

        title_box.append(filter_btn)

        # 3. Set the combined box as the title widget of the HeaderBar
        header_bar.set_title_widget(title_box)
        
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        # 3. Create the ScrolledWindow and Button Box
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.button_box.set_margin_top(12); self.button_box.set_margin_bottom(12)
        self.button_box.set_margin_start(12); self.button_box.set_margin_end(12)

        # Populate with sample buttons (mix of names for testing search)
        button_names = studentslist

        for name in button_names:
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.on_open_detail_page,name)
            self.button_box.append(btn)

        scrolled.set_child(self.button_box)
        self.stack.add_named(scrolled, "list_page")
        content_box.append(self.stack)
        self.set_content(content_box)
    def reset_filters(self, *unused):
        for button in self.filterlist:
            button.set_active(True)
            
    def on_filter_toggled(self, button, filter_key):
        # Update our dictionary state based on whether the checkbox is checked
        self.active_filters[filter_key] = button.get_active()
        self.on_search_changed(self.search_entry)
    def on_search_changed(self, entry):
        self.stack.set_visible_child_name("list_page")
        # Get the current search text in lowercase for case-insensitive matching
        query = entry.get_text().lower()

        # Iterate through all children in the Gtk.Box using GTK 4 methods
        child = self.button_box.get_first_child()
        while child is not None:
            if isinstance(child, Gtk.Button):
                label_text = child.get_label().lower()
                grade=self.get_data_on_person(child.get_label())['grade']
                # If query matches, show the button; otherwise, hide it
                if query in label_text and self.active_filters[str(grade)] is True:
                    child.set_visible(True)
                else:
                    child.set_visible(False)
                    
            child = child.get_next_sibling()
    def get_data_on_person(idk,name):
        return preloaded_student_info[name]
    def on_open_detail_page(self, button, item_name):
        # Create a unique page name using the button's name (slugified or just used directly)
        page_name = f"detail_{item_name.replace(' ','_')}"
        if not self.stack.get_child_by_name(page_name):
            detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            detail_box.set_margin_top(24); detail_box.set_margin_start(24); detail_box.set_margin_end(24)
            data=self.get_data_on_person(item_name)
            # 1. Create a horizontal box to hold the image on the left and title on the right
            header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            header_row.set_valign(Gtk.Align.CENTER)

            # 2. Create the image widget FIRST (so it goes on the left)
            image_path = data.get("xdg-open", f"./jpgs/grade{data['grade']}/{data['firstName']+' '+data['lastName']}.jpg") # Fallback path if missing in JSON
            avatar_image = Gtk.Image.new_from_file(image_path)
            avatar_image.set_pixel_size(160) # Size in pixels
            avatar_image.add_css_class("avatar") # Optional Libadwaita styling

            # 3. Create the title label SECOND (so it goes on the right of the image)
            title_label = Gtk.Label(label=f"{item_name}")
            title_label.add_css_class("title-2")
            title_label.set_halign(Gtk.Align.END)
            title_label.set_hexpand(True) # Fills remaining horizontal space

            # 4. Append to the header row in the desired order: Image -> Title
            header_row.append(avatar_image)
            header_row.append(title_label)
            
            desc_label = Gtk.Label(label=f"Grade: {data['grade']}")
            desc_label.add_css_class("title-3")
            #desc_label.set_vexpand(True)
            
            btn_row=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            btn_row.set_valign(Gtk.Align.CENTER)
            btn_row.set_hexpand(True)
            
            back_btn = Gtk.Button(label="← Back to List")
            back_btn.props.icon_name="go-previous-symbolic"
            back_btn.add_css_class("pill")
            back_btn.connect("clicked", lambda b: self.stack.set_visible_child_name("list_page"))
            back_btn.set_hexpand(True)
            back_btn.set_vexpand(True)
            btn_row.append(back_btn)
            
            namephoto_btns=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            namephoto_btns.add_css_class("linked")
            namephoto_btns.set_hexpand(True)
            
            cpy_btn=Gtk.Button(label="Copy Name")
            cpy_btn.props.icon_name="edit-copy-symbolic"
            cpy_btn.add_css_class("pill")
            cpy_btn.add_css_class("suggested-action")
            cpy_btn.connect("clicked", lambda b, n=item_name: pyperclip.copy(n))
            cpy_btn.set_hexpand(True)
            cpy_btn.set_vexpand(True)
            namephoto_btns.append(cpy_btn)
            
            img_btn=Gtk.Button(label="Open Image")
            img_btn.props.icon_name="folder-pictures-symbolic"
            img_btn.add_css_class("pill")
            img_btn.add_css_class("suggested-action")
            img_btn.connect("clicked", lambda b, grade=data['grade'],n=item_name: subprocess.Popen(command_to_open_img[platform.system()] % f"./jpgs/grade{grade}/{item_name}.jpg", shell=True))
            img_btn.set_hexpand(True)
            img_btn.set_vexpand(True)
            namephoto_btns.append(img_btn)
            
            btn_row.append(namephoto_btns)
            
            detail_box.append(header_row)
            detail_box.append(desc_label)
            
            detail_box.append(btn_row)

            self.stack.add_named(detail_box, page_name)

        # 4. Switch to the target page
        self.stack.set_visible_child_name(page_name)


class SearchApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.taylor.whhsroster")

    def do_activate(self):
        win = SearchableButtonWindow(application=self)
        win.present()

if __name__ == "__main__":
    app = SearchApp()
    app.run(None)
