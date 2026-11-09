# Fun Interactive Calculator GUI using tkinter

import tkinter as tk
from tkinter import font as tkfont


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Fun Calculator")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.expression = ""
        self.history = []

        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ---------- UI ----------
    def _build_display(self):
        self.display_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.display_frame.pack(fill="x", padx=16, pady=(18, 6))

        self.history_label = tk.Label(
            self.display_frame, text="", bg="#1e1e2e", fg="#6c6c8a",
            font=("Segoe UI", 10), anchor="e"
        )
        self.history_label.pack(fill="x")

        self.display = tk.Label(
            self.display_frame, text="0", bg="#1e1e2e", fg="#ffffff",
            font=("Segoe UI", 34, "bold"), anchor="e", padx=4, pady=6
        )
        self.display.pack(fill="x")

    def _build_buttons(self):
        self.buttons_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.buttons_frame.pack(expand=True, fill="both", padx=14, pady=10)

        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # (text, row, col, colspan, fg, bg, kind)
        buttons = [
            ("C",  0, 0, 1, "#ffffff", "#e64553", "clear"),
            ("⌫",  0, 1, 1, "#ffffff", "#45475a", "edit"),
            ("%",  0, 2, 1, "#ffffff", "#45475a", "op"),
            ("÷",  0, 3, 1, "#ffffff", "#f38ba8", "op"),

            ("7",  1, 0, 1, "#ffffff", "#313244", "num"),
            ("8",  1, 1, 1, "#ffffff", "#313244", "num"),
            ("9",  1, 2, 1, "#ffffff", "#313244", "num"),
            ("×",  1, 3, 1, "#ffffff", "#f38ba8", "op"),

            ("4",  2, 0, 1, "#ffffff", "#313244", "num"),
            ("5",  2, 1, 1, "#ffffff", "#313244", "num"),
            ("6",  2, 2, 1, "#ffffff", "#313244", "num"),
            ("−",  2, 3, 1, "#ffffff", "#f38ba8", "op"),

            ("1",  3, 0, 1, "#ffffff", "#313244", "num"),
            ("2",  3, 1, 1, "#ffffff", "#313244", "num"),
            ("3",  3, 2, 1, "#ffffff", "#313244", "num"),
            ("+",  3, 3, 1, "#ffffff", "#f38ba8", "op"),

            ("±",  4, 0, 1, "#ffffff", "#45475a", "neg"),
            ("0",  4, 1, 1, "#ffffff", "#313244", "num"),
            (".",  4, 2, 1, "#ffffff", "#313244", "num"),
            ("=",  4, 3, 1, "#ffffff", "#a6e3a1", "equals"),
        ]

        self._widgets = {}
        for text, r, c, cs, fg, bg, kind in buttons:
            btn = tk.Button(
                self.buttons_frame, text=text, fg=fg, bg=bg,
                activeforeground=fg, activebackground=self._lighten(bg),
                font=("Segoe UI", 16, "bold"), relief="flat", bd=0,
                cursor="hand2",
                command=lambda t=text, k=kind: self._on_click(t, k)
            )
            btn.grid(row=r, column=c, columnspan=cs, sticky="nsew",
                     padx=3, pady=3)
            self._bind_hover(btn, bg, fg)
            self._widgets[text] = btn

        # History button
        hist_btn = tk.Button(
            self.root, text="📜 History", bg="#45475a", fg="#cdd6f4",
            activebackground="#585b70", font=("Segoe UI", 10),
            relief="flat", bd=0, cursor="hand2",
            command=self._show_history
        )
        hist_btn.pack(fill="x", padx=14, pady=(0, 12))

    def _bind_hover(self, btn, base_bg, fg):
        hover_bg = self._lighten(base_bg)

        def on_enter(e):
            btn.configure(bg=hover_bg)

        def on_leave(e):
            btn.configure(bg=base_bg)

        def on_press(e):
            btn.configure(bg="#f9e2af", fg="#1e1e2e")

        def on_release(e):
            btn.configure(bg=hover_bg, fg=fg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress>", on_press)
        btn.bind("<ButtonRelease>", on_release)

    @staticmethod
    def _lighten(hex_color):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (min(255, c + 30) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ---------- Keyboard ----------
    def _bind_keyboard(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        char = event.char
        keysym = event.keysym

        if char in "0123456789":
            self._on_click(char, "num")
        elif char in "+-*/.%":
            mapping = {"*": "×", "/": "÷", "-": "−"}
            self._on_click(mapping.get(char, char), "op")
        elif char == ".":
            self._on_click(".", "num")
        elif char in ("\r", "\n") or keysym == "Return":
            self._on_click("=", "equals")
        elif keysym == "BackSpace":
            self._on_click("⌫", "edit")
        elif keysym == "Escape":
            self._on_click("C", "clear")

    # ---------- Logic ----------
    def _on_click(self, text, kind):
        if kind == "clear":
            self.expression = ""
            self._update_display("0")
            return

        if kind == "edit":
            self.expression = self.expression[:-1]
            self._update_display(self.expression or "0")
            return

        if kind == "neg":
            if self.expression:
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
                self._update_display(self.expression)
            return

        if kind == "equals":
            self._evaluate()
            return

        # percent: turn "50" into "0.5" style shortcut for simple cases
        if text == "%":
            try:
                value = float(self.expression or 0) / 100
                self.expression = self._format_number(value)
                self._update_display(self.expression)
            except ValueError:
                pass
            return

        if kind == "op":
            if not self.expression and text != "−":
                return
            # avoid stacking operators
            if self.expression and self.expression[-1] in "+−×÷":
                self.expression = self.expression[:-1]
            self.expression += text
            self._update_display(self.expression)
            return

        if kind == "num":
            if text == "." and "." in self.expression.split("+−×÷")[-1]:
                return
            self.expression += text
            self._update_display(self.expression)

    def _evaluate(self):
        if not self.expression:
            return
        try:
            expr = (self.expression
                    .replace("×", "*")
                    .replace("÷", "/")
                    .replace("−", "-"))
            # handle trailing operator
            if expr and expr[-1] in "+-*/.":
                expr = expr[:-1]
            if not expr:
                return
            result = eval(expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and result == int(result):
                result = int(result)
            shown = self._format_number(result)
            self.history.append(f"{self.expression} = {shown}")
            self.expression = shown
            self._update_display(shown)
            self._celebrate()
        except ZeroDivisionError:
            self._update_display("Cannot divide by 0! 😱")
            self.expression = ""
        except Exception:
            self._update_display("Oops! 😵")
            self.expression = ""

    @staticmethod
    def _format_number(value):
        if isinstance(value, float) and value == int(value):
            value = int(value)
        text = str(value)
        if len(text) > 14:
            text = f"{float(value):.8g}"
        return text

    def _update_display(self, text):
        size = 34 if len(str(text)) <= 12 else 24
        self.display.configure(text=text, font=("Segoe UI", size, "bold"))

    def _celebrate(self):
        # quick pop of color on the display
        original = "#1e1e2e"
        self.display_frame.configure(bg="#313244")
        self.display.configure(bg="#313244")
        self.history_label.configure(bg="#313244")
        self.root.after(120, lambda: self._restore_display(original))

    def _restore_display(self, color):
        self.display_frame.configure(bg=color)
        self.display.configure(bg=color)
        self.history_label.configure(bg=color)

    def _show_history(self):
        win = tk.Toplevel(self.root)
        win.title("Calculation History")
        win.geometry("320x360")
        win.configure(bg="#181825")

        tk.Label(
            win, text="📜 History", bg="#181825", fg="#f9e2af",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        if self.history:
            for item in self.history[-15:]:
                tk.Label(
                    win, text=item, bg="#181825", fg="#cdd6f4",
                    font=("Segoe UI", 11), anchor="w"
                ).pack(fill="x", padx=18, pady=2)
        else:
            tk.Label(
                win, text="No calculations yet", bg="#181825",
                fg="#6c6c8a", font=("Segoe UI", 11, "italic")
            ).pack(pady=20)

        tk.Button(
            win, text="Clear", bg="#e64553", fg="white", relief="flat",
            font=("Segoe UI", 10), cursor="hand2",
            command=lambda: (self.history.clear(), win.destroy())
        ).pack(pady=12)


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
