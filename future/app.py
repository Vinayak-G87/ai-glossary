from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk

from glossary import ENTRIES, Entry, categories, search


COLORS = {
    "paper": "#f4f1e8",
    "surface": "#fffdf7",
    "ink": "#202622",
    "muted": "#68706a",
    "line": "#d9d4c7",
    "accent": "#db5b3f",
    "accent_dark": "#a73d29",
    "green": "#32665a",
    "select": "#f3c85b",
}


class GlossaryWidget:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.results: list[Entry] = []
        self.query = tk.StringVar()
        self.category = tk.StringVar(value="All")
        self.pinned = tk.BooleanVar(value=True)
        self.count = tk.StringVar()

        self._configure_window()
        self._configure_styles()
        self._build_ui()
        self._bind_keys()
        self.refresh_results()
        self.search_entry.focus_set()

    def _configure_window(self) -> None:
        self.root.title("AI Glossary")
        self.root.geometry("380x520")
        self.root.minsize(330, 430)
        self.root.configure(bg=COLORS["paper"])
        self.root.attributes("-topmost", True)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Glossary.TCombobox",
            fieldbackground=COLORS["surface"],
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            bordercolor=COLORS["line"],
            arrowcolor=COLORS["green"],
            padding=5,
        )
        style.map("Glossary.TCombobox", bordercolor=[("focus", COLORS["green"])])
        style.configure(
            "Pin.TCheckbutton",
            background=COLORS["paper"],
            foreground=COLORS["muted"],
            font=("DejaVu Sans", 9),
        )
        style.map("Pin.TCheckbutton", foreground=[("active", COLORS["ink"])])

    def _build_ui(self) -> None:
        shell = tk.Frame(self.root, bg=COLORS["paper"], padx=14, pady=12)
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, bg=COLORS["paper"])
        header.pack(fill="x", pady=(0, 10))
        tk.Label(
            header,
            text="AI GLOSSARY",
            bg=COLORS["paper"],
            fg=COLORS["ink"],
            font=("DejaVu Serif", 16, "bold"),
        ).pack(side="left")
        ttk.Checkbutton(
            header,
            text="Keep on top",
            variable=self.pinned,
            command=self.toggle_pin,
            style="Pin.TCheckbutton",
            takefocus=False,
        ).pack(side="right")

        search_row = tk.Frame(shell, bg=COLORS["paper"])
        search_row.pack(fill="x", pady=(0, 8))
        self.search_entry = tk.Entry(
            search_row,
            textvariable=self.query,
            relief="flat",
            bg=COLORS["surface"],
            fg=COLORS["ink"],
            insertbackground=COLORS["accent"],
            highlightthickness=1,
            highlightbackground=COLORS["line"],
            highlightcolor=COLORS["accent"],
            font=("DejaVu Sans", 11),
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.query.trace_add("write", lambda *_: self.refresh_results())
        tk.Button(
            search_row,
            text="Clear",
            command=self.clear_search,
            relief="flat",
            bd=0,
            bg=COLORS["paper"],
            activebackground=COLORS["paper"],
            fg=COLORS["accent_dark"],
            activeforeground=COLORS["ink"],
            font=("DejaVu Sans", 9, "bold"),
            cursor="hand2",
            padx=8,
        ).pack(side="right")

        filter_row = tk.Frame(shell, bg=COLORS["paper"])
        filter_row.pack(fill="x", pady=(0, 8))
        self.category_box = ttk.Combobox(
            filter_row,
            textvariable=self.category,
            values=categories(),
            state="readonly",
            style="Glossary.TCombobox",
            width=17,
        )
        self.category_box.pack(side="left")
        self.category_box.bind("<<ComboboxSelected>>", lambda _: self.refresh_results())
        tk.Label(
            filter_row,
            textvariable=self.count,
            bg=COLORS["paper"],
            fg=COLORS["muted"],
            font=("DejaVu Sans", 9),
        ).pack(side="left", padx=9)
        tk.Button(
            filter_row,
            text="Surprise me",
            command=self.show_random,
            relief="flat",
            bd=0,
            bg=COLORS["green"],
            activebackground=COLORS["ink"],
            fg="white",
            activeforeground="white",
            font=("DejaVu Sans", 9, "bold"),
            cursor="hand2",
            padx=9,
            pady=5,
        ).pack(side="right")

        list_frame = tk.Frame(shell, bg=COLORS["line"], padx=1, pady=1)
        list_frame.pack(fill="x")
        self.result_list = tk.Listbox(
            list_frame,
            height=6,
            relief="flat",
            bd=0,
            bg=COLORS["surface"],
            fg=COLORS["ink"],
            selectbackground=COLORS["select"],
            selectforeground=COLORS["ink"],
            activestyle="none",
            highlightthickness=0,
            font=("DejaVu Sans", 10),
            exportselection=False,
        )
        self.result_list.pack(fill="x")
        self.result_list.bind("<<ListboxSelect>>", self.show_selected)

        self.detail = tk.Frame(shell, bg=COLORS["surface"], padx=14, pady=12)
        self.detail.pack(fill="both", expand=True, pady=(8, 0))
        self.category_label = tk.Label(
            self.detail,
            bg=COLORS["surface"],
            fg=COLORS["accent_dark"],
            font=("DejaVu Sans", 8, "bold"),
            anchor="w",
        )
        self.category_label.pack(fill="x")
        self.term_label = tk.Label(
            self.detail,
            bg=COLORS["surface"],
            fg=COLORS["ink"],
            font=("DejaVu Serif", 15, "bold"),
            anchor="w",
            justify="left",
            wraplength=310,
        )
        self.term_label.pack(fill="x", pady=(2, 7))
        self.meaning_label = self._detail_label(COLORS["ink"], 10)
        self.meaning_label.pack(fill="x")
        self.example_label = self._detail_label(COLORS["muted"], 9, italic=True)
        self.example_label.pack(fill="x", pady=(9, 0))
        self.importance_label = self._detail_label(COLORS["ink"], 9)
        self.importance_label.pack(fill="x", pady=(9, 0))
        self.related_label = self._detail_label(COLORS["green"], 9)
        self.related_label.pack(fill="x", pady=(9, 0))

        self.detail.bind("<Configure>", self._update_wraplength)

    def _detail_label(self, color: str, size: int, italic: bool = False) -> tk.Label:
        return tk.Label(
            self.detail,
            bg=COLORS["surface"],
            fg=color,
            font=("DejaVu Sans", size, "italic" if italic else "normal"),
            anchor="nw",
            justify="left",
            wraplength=310,
        )

    def _bind_keys(self) -> None:
        self.root.bind("<Control-l>", lambda _: self.focus_search())
        self.root.bind("<Control-f>", lambda _: self.focus_search())
        self.root.bind("<Escape>", lambda _: self.clear_search())
        self.search_entry.bind("<Down>", self.focus_results)
        self.result_list.bind("<Return>", lambda _: self.focus_search())
        self.root.bind("<Control-r>", lambda _: self.show_random())

    def refresh_results(self) -> None:
        self.results = search(self.query.get(), self.category.get())
        self.result_list.delete(0, tk.END)
        for entry in self.results:
            self.result_list.insert(tk.END, f"  {entry.term}")

        total = len(self.results)
        self.count.set(f"{total} term" if total == 1 else f"{total} terms")
        if self.results:
            self.result_list.selection_set(0)
            self.result_list.activate(0)
            self._show_entry(self.results[0])
        else:
            self._show_empty()

    def show_selected(self, _: tk.Event[tk.Listbox]) -> None:
        selected = self.result_list.curselection()
        if selected:
            self._show_entry(self.results[selected[0]])

    def _show_entry(self, entry: Entry) -> None:
        self.category_label.config(text=entry.category.upper())
        self.term_label.config(text=entry.term)
        self.meaning_label.config(text=entry.meaning)
        self.example_label.config(text=f"Example: {entry.example}")
        self.importance_label.config(
            text=f"Why it matters: {entry.why_it_matters}" if entry.why_it_matters else ""
        )
        related = "  /  ".join(entry.related)
        self.related_label.config(text=f"Related: {related}" if related else "")

    def _show_empty(self) -> None:
        self.category_label.config(text="NO MATCH")
        self.term_label.config(text="Try a broader search")
        self.meaning_label.config(text="Search by a term, category, or words from its meaning.")
        self.example_label.config(text="")
        self.importance_label.config(text="")
        self.related_label.config(text="")

    def _update_wraplength(self, event: tk.Event[tk.Frame]) -> None:
        wraplength = max(200, event.width - 28)
        for label in (
            self.term_label,
            self.meaning_label,
            self.example_label,
            self.importance_label,
            self.related_label,
        ):
            label.config(wraplength=wraplength)

    def focus_results(self, _: tk.Event[tk.Entry]) -> str:
        if self.results:
            self.result_list.focus_set()
            self.result_list.selection_clear(0, tk.END)
            self.result_list.selection_set(0)
        return "break"

    def focus_search(self) -> str:
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
        return "break"

    def clear_search(self) -> str:
        if self.query.get():
            self.query.set("")
        elif self.category.get() != "All":
            self.category.set("All")
            self.refresh_results()
        self.search_entry.focus_set()
        return "break"

    def show_random(self) -> None:
        entry = random.choice(ENTRIES)
        self.category.set("All")
        self.query.set(entry.term)

    def toggle_pin(self) -> None:
        self.root.attributes("-topmost", self.pinned.get())


def main() -> None:
    root = tk.Tk()
    GlossaryWidget(root)
    root.mainloop()


if __name__ == "__main__":
    main()