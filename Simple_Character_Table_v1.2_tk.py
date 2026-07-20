#!/usr/bin/env python3
"""
Tablica Znaków Unicode
Alternatywa dla windowsowskiego charmap.exe
Wymaga tylko Python 3 (wbudowany tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import unicodedata
import os
import sys
import json

APP_VERSION = "v1.2"

LANG = {
    "en": {
        "title": "Simple Character Table",
        "category": "Category:",
        "search": "Search:",
        "count_chars": "{} characters",
        "count_char": "{} character",
        "no_name": "(no name)",
        "click_hint": "Click a character to see details",
        "copy_char": "📋  Copy character",
        "copy_seq": "Copy sequence",
        "copied": "✓ Copied!",
        "favorites": "⭐ Favorites",
        "add_to_fav": "Add to favorites",
        "remove_from_fav": "Remove from favorites",
        "about": "About",
        "about_title": "About Simple Character Table",
        "program_name": "Simple Character Table",
        "version": "Version:",
        "author": "Author:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Search all categories",
        "history": "9 History",
        "options": "⋮",
        "export_fav": "Export favorites…",
        "import_fav": "Import favorites…",
        "clear_history": "Clear history",
        "export_title": "Export favorites",
        "import_title": "Import favorites",
        "export_success": "Exported {} favorite(s) to:\n{}",
        "import_success": "Imported {} new favorite(s).",
        "export_error": "Export failed:\n{}",
        "import_error": "Import failed:\n{}",
        "no_favorites": "No favorites yet. Right-click a character to add one.",
        "no_history": "No characters copied yet.",
        "shortcuts_hint": "Ctrl+C: copy selected   •   Ctrl+F: focus search   •   Esc: clear search",
        "categories": [
            "Basic Latin",
            "Latin Extended",
            "IPA Phonetic Alphabet",
            "Greek and Coptic",
            "Cyrillic",
            "Hebrew",
            "Arabic",
            "Currency",
            "Letterlike Symbols",
            "Punctuation",
            "Arrows",
            "Mathematical",
            "Misc Technical",
            "Geometric Shapes",
            "Misc Symbols",
            "Dingbats",
            "Emoji (Basic)",
            "Emoji (Transport)",
            "Emoji (Faces/Gestures)",
            "Mahjong and Cards"
        ]
    },
    "pl": {
        "title": "Simple Character Table",
        "category": "Kategoria:",
        "search": "Szukaj:",
        "count_chars": "{} znaków",
        "count_char": "{} znak",
        "no_name": "(brak nazwy)",
        "click_hint": "Kliknij znak, aby zobaczyć szczegóły",
        "copy_char": "📋  Kopiuj znak",
        "copy_seq": "Kopiuj sekwencję",
        "copied": "✓ Skopiowano!",
        "favorites": "⭐ Ulubione",
        "add_to_fav": "Dodaj do ulubionych",
        "remove_from_fav": "Usuń z ulubionych",
        "about": "O programie",
        "about_title": "O programie Simple Character Table",
        "program_name": "Simple Character Table",
        "version": "Wersja:",
        "author": "Autor:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Szukaj we wszystkich kategoriach",
        "history": "9 Historia",
        "options": "⋮",
        "export_fav": "Eksportuj ulubione…",
        "import_fav": "Importuj ulubione…",
        "clear_history": "Wyczyść historię",
        "export_title": "Eksportuj ulubione",
        "import_title": "Importuj ulubione",
        "export_success": "Wyeksportowano {} ulubionych do:\n{}",
        "import_success": "Zaimportowano {} nowych ulubionych.",
        "export_error": "Eksport nie powiódł się:\n{}",
        "import_error": "Import nie powiódł się:\n{}",
        "no_favorites": "Brak ulubionych. Kliknij prawym przyciskiem na znak, aby go dodać.",
        "no_history": "Nie skopiowano jeszcze żadnego znaku.",
        "shortcuts_hint": "Ctrl+C: kopiuj zaznaczony   •   Ctrl+F: focus na szukaj   •   Esc: wyczyść szukanie",
        "categories": [
            "Łacińskie podstawowe",
            "Łacińskie rozszerzone",
            "Alfabet fonetyczny (IPA)",
            "Grecki i koptyjski",
            "Cyrylica",
            "Hebrajski",
            "Arabski",
            "Waluty",
            "Literopodobne symbole",
            "Znaki interpunkcji",
            "Strzałki",
            "Matematyczne",
            "Różne techniczne",
            "Geometryczne kształty",
            "Różne symbole",
            "Dingbats",
            "Emoji (podstawowe)",
            "Emoji (transport)",
            "Emoji (twarze/gesty)",
            "Mahjong i karty"
        ]
    }
}

CATEGORIES = [
    ("Basic Latin",     0x0020, 0x007E),
    ("Latin Extended",    0x00C0, 0x02AF),
    ("IPA Phonetic Alphabet", 0x0250, 0x02AF),
    ("Greek and Coptic",       0x0370, 0x03FF),
    ("Cyrillic",                 0x0400, 0x04FF),
    ("Hebrew",                0x0590, 0x05FF),
    ("Arabic",                  0x0600, 0x06FF),
    ("Currency",                   0x20A0, 0x20CF),
    ("Letterlike Symbols",    0x2100, 0x214F),
    ("Punctuation",       0x2000, 0x206F),
    ("Arrows",                 0x2190, 0x21FF),
    ("Mathematical",             0x2200, 0x22FF),
    ("Misc Technical",         0x2300, 0x23FF),
    ("Geometric Shapes",    0x25A0, 0x25FF),
    ("Misc Symbols",            0x2600, 0x26FF),
    ("Dingbats",                 0x2700, 0x27BF),
    ("Emoji (Basic)",       0x1F300, 0x1F5FF),
    ("Emoji (Transport)",        0x1F680, 0x1F6FF),
    ("Emoji (Faces/Gestures)",     0x1F900, 0x1F9FF),
    ("Mahjong and Cards",          0x1F000, 0x1F0FF),
]

# ── Modern UI theme ──────────────────────────────────────────────────────────
FONT_FAMILY = "Segoe UI"
FONT_NORMAL = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)
FONT_TINY = (FONT_FAMILY, 8)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_TITLE = (FONT_FAMILY, 13, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
FONT_CHAR = (FONT_FAMILY, 14)
FONT_PREVIEW = (FONT_FAMILY, 34)
FONT_MONO = ("Consolas", 10)

BG = "#f3f4f9"            
PANEL_BG = "#ffffff"       
BORDER = "#e1e4ec"         
TEXT = "#1e2130"           
TEXT_MUTED = "#767c8c"     
TEXT_SUBTLE = "#9aa0ad"

ACCENT = "#4f46e5"         
ACCENT_HOVER = "#4338ca"
ACCENT_LIGHT = "#ecebfd"   

BTN_BG = "#ffffff"
BTN_HOVER = "#eef0f7"
BTN_BORDER = "#dadde6"
BTN_ACTIVE_BG = "#e3e0fb"  

CHAR_BTN_BG = "#ffffff"
CHAR_BTN_HOVER = "#ecebfd"
CHAR_BTN_SELECTED = "#4f46e5"
CHAR_BTN_SELECTED_FG = "#ffffff"
CHAR_BTN_FAV = "#fff3cd"
CHAR_BTN_FAV_HOVER = "#ffe9a8"

SUCCESS_BG = "#dcfce7"
SUCCESS_TEXT = "#15803d"

SCROLLBAR_BG = "#c7cbd8"
SCROLLBAR_TROUGH = "#f3f4f9"

TOOLTIP_BG = "#1e2130"
TOOLTIP_FG = "#ffffff"


def _add_hover(btn, hover_bg, normal_bg=None):
    if normal_bg is not None:
        btn._normal_bg = normal_bg
    else:
        btn._normal_bg = btn.cget("bg")

    def _on_enter(_event=None):
        btn.config(bg=hover_bg)

    def _on_leave(_event=None):
        btn.config(bg=getattr(btn, "_normal_bg", hover_bg))

    btn.bind("<Enter>", _on_enter, add="+")
    btn.bind("<Leave>", _on_leave, add="+")


def set_normal_bg(btn, color):
    btn._normal_bg = color
    btn.config(bg=color)

_all_chars_cache = None


def get_chars(start, end):
    result = []
    for cp in range(start, end + 1):
        try:
            ch = chr(cp)
            cat = unicodedata.category(ch)
            if cat not in ("Cc", "Cs", "Co"):
                result.append(cp)
        except (ValueError, OverflowError):
            pass
    return result


def get_all_chars():
    global _all_chars_cache
    if _all_chars_cache is None:
        seen = {}
        for _, start, end in CATEGORIES:
            for cp in get_chars(start, end):
                seen[cp] = True
        _all_chars_cache = sorted(seen.keys())
    return _all_chars_cache


def char_name(cp, lang="en"):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return LANG[lang]["no_name"]


def get_resource_path(filename):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)


def get_app_data_dir():
    app_name = "SimpleCharacterTable"
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path


class ToolTip:
    def __init__(self, widget, text_func, delay=450):
        self.widget = widget
        self.text_func = text_func
        self.delay = delay
        self.tipwindow = None
        self.after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<Button-1>", self._hide, add="+")
        widget.bind("<Button-3>", self._hide, add="+")

    def _schedule(self, _event=None):
        self._cancel()
        self.after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        text = self.text_func()
        if not text or self.tipwindow is not None:
            return
        try:
            x = self.widget.winfo_rootx() + 10
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        except tk.TclError:
            return
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        try:
            tw.wm_attributes("-topmost", True)
        except tk.TclError:
            pass
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=text, justify="left", background=TOOLTIP_BG, foreground=TOOLTIP_FG,
            relief="flat", borderwidth=0, font=FONT_SMALL, padx=8, pady=5
        )
        label.pack()
        self.tipwindow = tw

    def _cancel(self):
        if self.after_id is not None:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def _hide(self, _event=None):
        self._cancel()
        if self.tipwindow is not None:
            self.tipwindow.destroy()
            self.tipwindow = None


class TablicaZnakow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.settings_file = os.path.join(get_app_data_dir(), "ustawienia.json")
        self.lang = self._load_settings().get("lang", "en")
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')

        ico_path = get_resource_path("tz-ico.ico")
        png_path = get_resource_path("tz-png.png")

        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except tk.TclError:
                pass
        elif os.path.exists(png_path):
            try:
                self.icon_img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, self.icon_img)
            except tk.TclError:
                pass

        window_width = 950
        window_height = 680
        self.minsize(860, 540)
        self.configure(bg=BG)
        self._setup_ttk_style()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.selected_cp = None
        self.char_buttons = []
        self.char_button_map = {}
        self.tooltips = []
        self.favorites = []
        self.history = []
        self.current_chars_list = []  # Cache aktualnej listy znaków do szybkiego przerysowania
        self.favorites_file = os.path.join(get_app_data_dir(), "ulubione.txt")
        self.history_file = os.path.join(get_app_data_dir(), "historia.txt")
        self.view_mode = "category"

        self._load_favorites()
        self._load_history()
        self._build_ui()
        self._bind_shortcuts()
        self._set_view_mode("category")

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save_settings(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump({"lang": self.lang}, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _setup_ttk_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=PANEL_BG, background=PANEL_BG, foreground=TEXT,
            arrowcolor=ACCENT, bordercolor=BORDER, lightcolor=PANEL_BG,
            darkcolor=PANEL_BG, padding=4, relief="flat",
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", PANEL_BG)],
            foreground=[("readonly", TEXT)],
            bordercolor=[("focus", ACCENT)],
        )
        self.option_add("*TCombobox*Listbox.background", PANEL_BG)
        self.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT_LIGHT)
        self.option_add("*TCombobox*Listbox.selectForeground", TEXT)
        self.option_add("*TCombobox*Listbox.font", FONT_NORMAL)

        style.configure("TCheckbutton", background=BG, foreground=TEXT, font=FONT_SMALL)
        style.map("TCheckbutton", background=[("active", BG)])

        style.configure(
            "Vertical.TScrollbar",
            background=SCROLLBAR_BG, troughcolor=SCROLLBAR_TROUGH,
            bordercolor=BG, arrowcolor=TEXT_MUTED, relief="flat", width=12,
        )
        style.map("Vertical.TScrollbar", background=[("active", ACCENT)])

    def _flat_button(self, parent, text, command, font=FONT_NORMAL, padx=12, pady=6,
                      bg=BTN_BG, hover=BTN_HOVER, fg=TEXT, state="normal"):
        btn = tk.Button(
            parent, text=text, font=font, command=command,
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            disabledforeground=TEXT_SUBTLE,
            relief="flat", bd=0, padx=padx, pady=pady, cursor="hand2",
            highlightthickness=1, highlightbackground=BTN_BORDER, highlightcolor=BTN_BORDER,
            state=state,
        )
        _add_hover(btn, hover, normal_bg=bg)
        return btn

    def _show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title(LANG[self.lang]["about_title"])
        about_window.resizable(False, False)
        about_window.configure(bg=PANEL_BG)

        window_width = 360
        window_height = 290
        screen_width = about_window.winfo_screenwidth()
        screen_height = about_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        about_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        about_window.transient(self)
        about_window.grab_set()

        accent_bar = tk.Frame(about_window, bg=ACCENT, height=4)
        accent_bar.pack(fill="x", side="top")

        frame = tk.Frame(about_window, bg=PANEL_BG, padx=20, pady=18)
        frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(frame, bg=PANEL_BG)
        header_frame.pack(fill="x", pady=(0, 10))

        try:
            png_path = get_resource_path("tz-png.png")
            if os.path.exists(png_path):
                icon_img = tk.PhotoImage(file=png_path)
                about_window._icon_img_ref = icon_img.subsample(6, 6)
                icon_label = tk.Label(header_frame, image=about_window._icon_img_ref, bg=PANEL_BG)
                icon_label.pack(side="left", padx=(0, 10))
        except Exception:
            pass

        name_version_frame = tk.Frame(header_frame, bg=PANEL_BG)
        name_version_frame.pack(side="left", fill="x", anchor="w")

        program_label = tk.Label(name_version_frame, text=LANG[self.lang]["program_name"],
                                 font=FONT_TITLE, bg=PANEL_BG, fg=TEXT, anchor="w")
        program_label.pack(side="left")

        version_badge = tk.Label(
            name_version_frame, text=APP_VERSION, font=(FONT_FAMILY, 9, "bold"),
            bg=ACCENT_LIGHT, fg=ACCENT, padx=7, pady=1,
        )
        version_badge.pack(side="left", padx=(8, 0))

        version_label = tk.Label(frame, text=f"{LANG[self.lang]['version']} {APP_VERSION}",
                                 font=FONT_SMALL, bg=PANEL_BG, fg=TEXT_MUTED, anchor="w")
        version_label.pack(fill="x", pady=(2, 6))

        author_label = tk.Label(frame, text=f"{LANG[self.lang]['author']} Sebastian Januchowski",
                                font=FONT_NORMAL, bg=PANEL_BG, fg=TEXT, anchor="w")
        author_label.pack(fill="x", pady=3)

        mail_label = tk.Label(frame, text=f"{LANG[self.lang]['mail']} polsoft.its@mail.com",
                              font=FONT_NORMAL, bg=PANEL_BG, anchor="w", fg=ACCENT, cursor="hand2")
        mail_label.pack(fill="x", pady=3)
        mail_label.bind("<Button-1>", lambda e: self._open_url("mailto:polsoft.its@mail.com"))

        github_label = tk.Label(frame, text=f"{LANG[self.lang]['github']} polsoft.ITS™",
                                font=FONT_NORMAL, bg=PANEL_BG, anchor="w", fg=ACCENT, cursor="hand2")
        github_label.pack(fill="x", pady=3)
        github_label.bind("<Button-1>", lambda e: self._open_url("https://github.com/polsoft-IT"))

        ok_btn = self._flat_button(
            frame, "OK", about_window.destroy, font=FONT_SMALL,
            padx=18, pady=5, bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff",
        )
        ok_btn.pack(pady=(16, 4))

    def _open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def _switch_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')
        self._save_settings()
        self._update_ui_text()
        self.search_var.set("")
        self._refresh_current_view()

    def _update_ui_text(self):
        self.cat_label.config(text=LANG[self.lang]["category"])
        self.search_label.config(text=LANG[self.lang]["search"])
        self.fav_btn.config(text=LANG[self.lang]["favorites"])
        self.history_btn.config(text=LANG[self.lang]["history"])
        self.global_chk.config(text=LANG[self.lang]["global_search"])
        self.lang_btn.config(text="PL" if self.lang == "en" else "EN")
        self.about_btn.config(text=LANG[self.lang]["about"])
        self.options_btn.config(text=LANG[self.lang]["options"])
        self.shortcuts_label.config(text=LANG[self.lang]["shortcuts_hint"])
        if self.selected_cp is None:
            self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.copy_btn.config(text=LANG[self.lang]["copy_char"])
        self.copy_seq_btn.config(text=LANG[self.lang]["copy_seq"])
        current_idx = self.cat_combo.current()
        self.cat_combo.config(values=LANG[self.lang]["categories"])
        self.cat_combo.current(current_idx)

    def _build_ui(self):
        # Główny kontener ustawiony na reagowanie na siatkę geometryczną
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        accent_bar = tk.Frame(self, bg=ACCENT, height=3)
        accent_bar.grid(row=0, column=0, sticky="ew")

        top_wrap = tk.Frame(self, bg=PANEL_BG, highlightthickness=1,
                             highlightbackground=BORDER, highlightcolor=BORDER)
        top_wrap.grid(row=1, column=0, sticky="ew")
        
        top = tk.Frame(top_wrap, bg=PANEL_BG, pady=10, padx=16)
        top.pack(fill="x", expand=True)

        row1 = tk.Frame(top, bg=PANEL_BG)
        row1.pack(fill="x", expand=True)
        row2 = tk.Frame(top, bg=PANEL_BG)
        row2.pack(fill="x", expand=True, pady=(10, 0))

        self.cat_label = tk.Label(row1, text=LANG[self.lang]["category"], bg=PANEL_BG, fg=TEXT, font=FONT_NORMAL)
        self.cat_label.pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(
            row1, textvariable=self.cat_var,
            values=LANG[self.lang]["categories"],
            state="readonly", width=24, font=FONT_NORMAL
        )
        self.cat_combo.current(0)
        self.cat_combo.pack(side="left", padx=(6, 16))
        self.cat_combo.bind("<<ComboboxSelected>>", self._on_category)

        self.search_label = tk.Label(row1, text=LANG[self.lang]["search"], bg=PANEL_BG, fg=TEXT, font=FONT_NORMAL)
        self.search_label.pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        self.search_entry = tk.Entry(
            row1, textvariable=self.search_var, font=FONT_NORMAL, width=18,
            relief="flat", bd=0, bg=PANEL_BG, fg=TEXT, insertbackground=TEXT,
            highlightthickness=1, highlightbackground=BTN_BORDER, highlightcolor=ACCENT,
        )
        self.search_entry.pack(side="left", padx=(6, 0), ipady=4)
        self.search_entry.bind("<Escape>", self._on_escape)

        self.global_search_var = tk.BooleanVar(value=False)
        self.global_chk = tk.Checkbutton(
            row1, text=LANG[self.lang]["global_search"], variable=self.global_search_var,
            command=self._on_search, bg=PANEL_BG, fg=TEXT, font=FONT_SMALL,
            activebackground=PANEL_BG, activeforeground=TEXT, selectcolor=PANEL_BG,
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self.global_chk.pack(side="left", padx=(10, 0))

        self.count_label = tk.Label(row1, text="", bg=PANEL_BG,
                                    font=FONT_SMALL, fg=TEXT_MUTED)
        self.count_label.pack(side="right")

        self.fav_btn = self._flat_button(row2, LANG[self.lang]["favorites"], self._toggle_favorites_panel,
                                          padx=12, pady=6)
        self.fav_btn.pack(side="left")

        self.history_btn = self._flat_button(row2, LANG[self.lang]["history"], self._toggle_history_panel,
                                              padx=12, pady=6)
        self.history_btn.pack(side="left", padx=(8, 0))

        self.options_btn = self._flat_button(row2, LANG[self.lang]["options"], self._show_options_menu,
                                              font=FONT_SUBTITLE, padx=10, pady=4)
        self.options_btn.pack(side="left", padx=(8, 0))

        self.about_btn = self._flat_button(row2, LANG[self.lang]["about"], self._show_about, padx=14, pady=6)
        self.about_btn.pack(side="right")

        self.lang_btn = self._flat_button(
            row2, "PL" if self.lang == "en" else "EN", self._switch_language,
            font=FONT_BOLD, padx=14, pady=6, bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff",
        )
        self.lang_btn.pack(side="right", padx=(8, 0))

        shortcuts_bar = tk.Frame(self, bg=BG, padx=16)
        shortcuts_bar.grid(row=2, column=0, sticky="ew")
        self.shortcuts_label = tk.Label(
            shortcuts_bar, text=LANG[self.lang]["shortcuts_hint"], bg=BG,
            font=FONT_TINY, fg=TEXT_SUBTLE, anchor="w"
        )
        self.shortcuts_label.pack(side="left", pady=(6, 4))

        # Kontener główny siatki znaków dopasowujący się do okna
        grid_frame = tk.Frame(self, bg=BG, padx=16)
        grid_frame.grid(row=3, column=0, sticky="nsew")
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(grid_frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(canvas, bg=BG)
        self.canvas_window = canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Kluczowe zdarzenie: dynamiczne przeliczanie kolumn przy zmianie rozmiaru okna
        canvas.bind("<Configure>", self._on_canvas_resize)

        def _on_mousewheel(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def _bind_mousewheel(_event=None):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mousewheel(_event=None):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)

        self.canvas = canvas

        # Panel dolny informacyjny (zawsze na dole okna)
        info_wrap = tk.Frame(self, bg=BG)
        info_wrap.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 14))
        info = tk.Frame(info_wrap, bg=PANEL_BG, padx=18, pady=14,
                        relief="flat", bd=0, highlightthickness=1,
                        highlightbackground=BORDER, highlightcolor=BORDER)
        info.pack(fill="x", expand=True)

        self.preview_label = tk.Label(
            info, text="", font=FONT_PREVIEW, bg=ACCENT_LIGHT, fg=ACCENT,
            width=2, anchor="center", relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER,
        )
        self.preview_label.grid(row=0, column=0, rowspan=2, padx=(0, 16), sticky="ns")

        self.name_label = tk.Label(
            info, text=LANG[self.lang]["click_hint"],
            font=FONT_BOLD, bg=PANEL_BG, fg=TEXT, anchor="w"
        )
        self.name_label.grid(row=0, column=1, sticky="w")

        self.code_label = tk.Label(
            info, text="", font=FONT_MONO, bg=PANEL_BG,
            fg=TEXT_MUTED, anchor="w"
        )
        self.code_label.grid(row=1, column=1, sticky="w", pady=(4, 0))

        self.copy_btn = self._flat_button(
            info, LANG[self.lang]["copy_char"], self._copy_char, padx=14, pady=6,
            bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff", state="disabled",
        )
        self.copy_btn.grid(row=0, column=2, rowspan=2, padx=(18, 0), sticky="e")

        self.copy_seq_btn = self._flat_button(
            info, LANG[self.lang]["copy_seq"], self._copy_seq, padx=12, pady=6, state="disabled",
        )
        self.copy_seq_btn.grid(row=0, column=3, rowspan=2, padx=(8, 0), sticky="e")

        info.columnconfigure(1, weight=1)

    def _bind_shortcuts(self):
        self.bind_all("<Control-c>", self._on_ctrl_c)
        self.bind_all("<Control-C>", self._on_ctrl_c)
        self.bind_all("<Control-f>", self._on_ctrl_f)
        self.bind_all("<Control-F>", self._on_ctrl_f)
        self.bind_all("<Escape>", self._on_escape)

    def _on_ctrl_c(self, event=None):
        focused = self.focus_get()
        if isinstance(focused, (tk.Entry, ttk.Entry)):
            return  
        if self.selected_cp is not None:
            self._copy_char()
        return "break"

    def _on_ctrl_f(self, event=None):
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
        self.search_entry.icursor(tk.END)
        return "break"

    def _on_escape(self, event=None):
        if self.search_var.get():
            self.search_var.set("")
        self.focus_set()
        return "break"

    def _current_category_chars(self):
        idx = self.cat_combo.current()
        if idx < 0:
            idx = 0
        _, start, end = CATEGORIES[idx]
        return get_chars(start, end)

    def _refresh_current_view(self):
        if self.view_mode == "favorites":
            self._render_grid(self.favorites)
        elif self.view_mode == "history":
            self._render_grid(self.history)
        else:
            self._on_search()

    def _on_category(self, event=None):
        self.search_var.set("")
        self._clear_selection()

    def _on_search(self, *args):
        q = self.search_var.get().strip().lower()

        if self.view_mode == "favorites":
            source = self.favorites
        elif self.view_mode == "history":
            source = self.history
        elif self.global_search_var.get() and q:
            source = get_all_chars()
        else:
            source = self._current_category_chars()

        if not q:
            self._render_grid(source)
            return

        filtered = []
        for cp in source:
            ch = chr(cp)
            hex_code = f"u+{cp:04x}"
            name = char_name(cp, self.lang).lower()
            if q in hex_code or q in str(cp) or q in ch.lower() or q in name:
                filtered.append(cp)
        self._render_grid(filtered)

    def _on_canvas_resize(self, event):
        # Aktualizacja szerokości wewnętrznego okna Canvasa
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        # Ponowne rozmieszczenie przycisków na podstawie nowej szerokości
        if hasattr(self, 'current_chars_list') and self.current_chars_list:
            self._arrange_buttons(event.width)

    def _render_grid(self, chars):
        self.current_chars_list = chars
        for tip in self.tooltips:
            tip._hide()
        self.tooltips.clear()
        for btn in self.char_buttons:
            btn.destroy()
        self.char_buttons.clear()
        self.char_button_map = {}
        self.selected_cp = None

        if not chars:
            self.count_label.config(text=LANG[self.lang]["count_char"].format(0))
            if self.view_mode == "favorites":
                empty_text = LANG[self.lang]["no_favorites"]
            elif self.view_mode == "history":
                empty_text = LANG[self.lang]["no_history"]
            else:
                empty_text = None
            if empty_text:
                placeholder = tk.Label(self.inner, text=empty_text, bg=BG,
                                       fg=TEXT_MUTED, font=FONT_NORMAL, wraplength=600, justify="left")
                placeholder.grid(row=0, column=0, sticky="w", pady=10, padx=4)
                self.char_buttons.append(placeholder)
            self.canvas.yview_moveto(0)
            return

        count_text = LANG[self.lang]["count_char"] if len(chars) == 1 else LANG[self.lang]["count_chars"]
        self.count_label.config(text=count_text.format(len(chars)))

        # Generowanie przycisków (wstępnie bez wywoływania .grid)
        for cp in chars:
            ch = chr(cp)
            is_fav = cp in self.favorites
            rest_bg = CHAR_BTN_FAV if is_fav else CHAR_BTN_BG
            btn = tk.Button(
                self.inner,
                text=ch,
                font=FONT_CHAR,
                width=2, height=1,
                relief="flat", bd=0,
                bg=rest_bg, fg=TEXT,
                activebackground=CHAR_BTN_HOVER, activeforeground=TEXT,
                highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                cursor="hand2",
                command=lambda c=cp: self._select(c)
            )
            _add_hover(btn, CHAR_BTN_FAV_HOVER if is_fav else CHAR_BTN_HOVER, normal_bg=rest_bg)
            btn.bind("<Button-3>", lambda e, c=cp: self._show_context_menu(e, c))
            self.char_buttons.append(btn)
            self.char_button_map[cp] = btn
            self.tooltips.append(
                ToolTip(btn, (lambda c=cp: f"{char_name(c, self.lang)}\nU+{c:04X}"))
            )

        # Rozmieść wygenerowane przyciski
        self._arrange_buttons(self.canvas.winfo_width())
        self.canvas.yview_moveto(0)

    def _arrange_buttons(self, width):
        if not self.char_buttons or not self.char_button_map:
            return
            
        # Obliczanie na bieżąco ile kolumn zmieści się w aktualnej szerokości okna
        btn_width = 46  # Przybliżona szerokość jednego kafelka z paddingiem
        cols = max(1, width // btn_width)

        for i, btn in enumerate(self.char_buttons):
            if isinstance(btn, tk.Button):
                btn.grid_forget()
                btn.grid(row=i // cols, column=i % cols, padx=3, pady=3, sticky="nsew")

        for col in range(cols):
            self.inner.columnconfigure(col, weight=1, minsize=42)
        
        # Wyczyszczenie starych, nieużywanych konfiguracji kolumn
        for col in range(cols, self.inner.grid_size()[0]):
            self.inner.columnconfigure(col, weight=0, minsize=0)

    def _select(self, cp):
        self.selected_cp = cp
        ch = chr(cp)
        name = char_name(cp, self.lang)
        hex4 = f"U+{cp:04X}"
        html_ent = f"&#{cp};"
        py_esc = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"

        self.preview_label.config(text=ch)
        self.name_label.config(text=name)
        self.code_label.config(
            text=f"{hex4}   HTML: {html_ent}   Python: {py_esc}   Dziesiętnie: {cp}"
        )
        self.copy_btn.config(state="normal")
        self.copy_seq_btn.config(state="normal")

        for btn_cp, btn in self.char_button_map.items():
            rest_bg = CHAR_BTN_FAV if btn_cp in self.favorites else CHAR_BTN_BG
            set_normal_bg(btn, rest_bg)
            btn.config(fg=TEXT)
        selected_btn = self.char_button_map.get(cp)
        if selected_btn is not None:
            selected_btn.config(bg=CHAR_BTN_SELECTED, fg=CHAR_BTN_SELECTED_FG)
            selected_btn._normal_bg = CHAR_BTN_SELECTED

    def _clear_selection(self):
        self.selected_cp = None
        self.preview_label.config(text="")
        self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.code_label.config(text="")
        self.copy_btn.config(state="disabled")
        self.copy_seq_btn.config(state="disabled")

    def _copy_char(self):
        if self.selected_cp is not None:
            self.clipboard_clear()
            self.clipboard_append(chr(self.selected_cp))
            self._add_to_history(self.selected_cp)
            self._flash_btn()

    def _copy_seq(self):
        if self.selected_cp is not None:
            cp = self.selected_cp
            seq = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
            self.clipboard_clear()
            self.clipboard_append(seq)
            self._add_to_history(cp)
            self._flash_btn(seq=True)

    def _load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.favorites.append(int(line))
                        except ValueError:
                            pass

    def _save_favorites(self):
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            for cp in self.favorites:
                f.write(f"{cp}\n")

    def _toggle_favorite(self, cp):
        if cp in self.favorites:
            self.favorites.remove(cp)
        else:
            self.favorites.append(cp)
        self._save_favorites()
        if self.view_mode == "favorites":
            self._refresh_current_view()
        elif cp in self.char_button_map:
            btn = self.char_button_map[cp]
            rest_bg = CHAR_BTN_FAV if cp in self.favorites else CHAR_BTN_BG
            hover_bg = CHAR_BTN_FAV_HOVER if cp in self.favorites else CHAR_BTN_HOVER
            if cp == self.selected_cp:
                btn._normal_bg = CHAR_BTN_SELECTED
            else:
                set_normal_bg(btn, rest_bg)
            _add_hover(btn, hover_bg, normal_bg=btn._normal_bg)

    def _export_favorites(self):
        if not self.favorites:
            messagebox.showinfo(LANG[self.lang]["export_title"], LANG[self.lang]["no_favorites"])
            return
        path = filedialog.asksaveasfilename(
            title=LANG[self.lang]["export_title"],
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Text", "*.txt")]
        )
        if not path:
            return
        try:
            if path.lower().endswith(".json"):
                data = [
                    {"cp": cp, "char": chr(cp), "name": char_name(cp, self.lang)}
                    for cp in self.favorites
                ]
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    for cp in self.favorites:
                        f.write(f"{cp}\n")
            messagebox.showinfo(
                LANG[self.lang]["export_title"],
                LANG[self.lang]["export_success"].format(len(self.favorites), path)
            )
        except OSError as e:
            messagebox.showerror(LANG[self.lang]["export_title"], LANG[self.lang]["export_error"].format(e))

    def _import_favorites(self):
        path = filedialog.askopenfilename(
            title=LANG[self.lang]["import_title"],
            filetypes=[("JSON/Text", "*.json *.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            added = 0
            if path.lower().endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    cp = item["cp"] if isinstance(item, dict) else int(item)
                    if cp not in self.favorites:
                        self.favorites.append(cp)
                        added += 1
            else:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                cp = int(line)
                            except ValueError:
                                continue
                            if cp not in self.favorites:
                                self.favorites.append(cp)
                                added += 1
            self._save_favorites()
            if self.view_mode == "favorites":
                self._refresh_current_view()
            messagebox.showinfo(
                LANG[self.lang]["import_title"], LANG[self.lang]["import_success"].format(added)
            )
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            messagebox.showerror(LANG[self.lang]["import_title"], LANG[self.lang]["import_error"].format(e))

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.history.append(int(line))
                        except ValueError:
                            pass

    def _save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            for cp in self.history:
                f.write(f"{cp}\n")

    def _add_to_history(self, cp):
        if cp in self.history:
            self.history.remove(cp)
        self.history.insert(0, cp)
        del self.history[HISTORY_MAX:]
        self._save_history()
        if self.view_mode == "history":
            self._refresh_current_view()

    def _clear_history(self):
        self.history = []
        self._save_history()
        if self.view_mode == "history":
            self._refresh_current_view()

    def _toggle_favorites_panel(self):
        self._set_view_mode("category" if self.view_mode == "favorites" else "favorites")

    def _toggle_history_panel(self):
        self._set_view_mode("category" if self.view_mode == "history" else "history")

    def _set_view_mode(self, mode):
        self.view_mode = mode
        if mode == "favorites":
            set_normal_bg(self.fav_btn, BTN_ACTIVE_BG)
            set_normal_bg(self.history_btn, BTN_BG)
            self.cat_combo.config(state="disabled")
            self.global_chk.config(state="disabled")
        elif mode == "history":
            set_normal_bg(self.fav_btn, BTN_BG)
            set_normal_bg(self.history_btn, BTN_ACTIVE_BG)
            self.cat_combo.config(state="disabled")
            self.global_chk.config(state="disabled")
        else:
            set_normal_bg(self.fav_btn, BTN_BG)
            set_normal_bg(self.history_btn, BTN_BG)
            self.cat_combo.config(state="readonly")
            self.global_chk.config(state="normal")
        self._clear_selection()
        self.search_var.set("")  

    def _make_menu(self):
        return tk.Menu(
            self, tearoff=0, bg=PANEL_BG, fg=TEXT, activebackground=ACCENT_LIGHT,
            activeforeground=TEXT, bd=0, relief="flat", font=FONT_NORMAL,
        )

    def _show_options_menu(self):
        menu = self._make_menu()
        menu.add_command(label=LANG[self.lang]["export_fav"], command=self._export_favorites)
        menu.add_command(label=LANG[self.lang]["import_fav"], command=self._import_favorites)
        menu.add_separator()
        menu.add_command(label=LANG[self.lang]["clear_history"], command=self._clear_history)
        x = self.options_btn.winfo_rootx()
        y = self.options_btn.winfo_rooty() + self.options_btn.winfo_height()
        menu.post(x, y)

    def _show_context_menu(self, event, cp):
        menu = self._make_menu()
        if cp in self.favorites:
            menu.add_command(label=LANG[self.lang]["remove_from_fav"], command=lambda: self._toggle_favorite(cp))
        else:
            menu.add_command(label=LANG[self.lang]["add_to_fav"], command=lambda: self._toggle_favorite(cp))
        menu.post(event.x_root, event.y_root)

    def _flash_btn(self, seq=False):
        btn = self.copy_seq_btn if seq else self.copy_btn
        orig = btn.cget("text")
        orig_bg = BTN_BG if seq else ACCENT
        btn.config(text=LANG[self.lang]["copied"], bg=SUCCESS_BG, fg=SUCCESS_TEXT)
        btn._normal_bg = SUCCESS_BG

        def _restore():
            btn.config(text=orig, bg=orig_bg, fg=TEXT if seq else "#ffffff")
            btn._normal_bg = orig_bg

        self.after(1200, _restore)


if __name__ == "__main__":
    app = TablicaZnakow()
    app.mainloop()