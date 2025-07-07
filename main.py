import math
import tkinter as tk
from tkinter import ttk, messagebox


class Calculator:
    def __init__(self):
        self.expression = ''  # 新增算式跟踪属性
        self.current_value = ""
        self.first_operand = None
        self.operator = None
        self.reset_after_operation = False
        self.angle_unit = 'degrees'  # 'degrees' or 'radians'

    def append_number(self, number):
        self.expression += str(number)
        if self.reset_after_operation:
            self.current_value = str(number)
            self.reset_after_operation = False
        else:
            self.current_value += str(number)
        return self.current_value

    def set_operator(self, operator):
        if self.operator and self.first_operand is not None:
            prev_result = self.calculate()
            self.expression = f'{prev_result} {operator} '
            self.first_operand = float(prev_result)
            self.operator = operator
        else:
            if self.current_value:
                self.expression += f' {self.current_value} {operator} '
                self.first_operand = float(self.current_value)
                self.operator = operator
                self.current_value = ''
        return None

    def get_current_expression(self):
        return self.expression

    def toggle_angle_unit(self):
        self.angle_unit = 'radians' if self.angle_unit == 'degrees' else 'degrees'
        return self.angle_unit

    def calculate(self):
        # 如果没有操作符，直接返回当前值
        if not self.operator:
            return self.current_value or "0"
        if not self.current_value:
            return "错误: 缺少操作数"
        if not self.first_operand:
            return "错误: 请先输入数字"
        if not self.operator:
            return self.current_value or "0"

        second_operand = float(self.current_value)
        result = 0

        try:
            if self.operator == "+":
                result = self.add(self.first_operand, second_operand)
            elif self.operator == "-":
                result = self.subtract(self.first_operand, second_operand)
            elif self.operator == "×":
                result = self.multiply(self.first_operand, second_operand)
            elif self.operator == "÷":
                result = self.divide(self.first_operand, second_operand)
            elif self.operator == "^":
                result = self.power(self.first_operand, second_operand)
            elif self.operator == "√":
                result = self.square_root(second_operand)
            elif self.operator == "∛":
                result = self.cube_root(second_operand)
            elif self.operator == "sin":
                result = self.sin(second_operand, self.angle_unit == 'radians')
            elif self.operator == "cos":
                result = self.cos(second_operand, self.angle_unit == 'radians')
            elif self.operator == "tan":
                result = self.tan(second_operand, self.angle_unit == 'radians')
        except Exception as e:
            return f"错误: {str(e)}"

        # 格式化结果，避免过多小数位
        formatted_result = "{0:.10f}".format(result).rstrip('0').rstrip('.') if '.' in "{0:.10f}".format(result) else str(int(result))
        self.current_value = formatted_result
        # 保留第一个操作数以支持连续运算
        self.first_operand = float(formatted_result)
        self.operator = None
        self.reset_after_operation = True
        return self.current_value

    def clear(self):
        self.current_value = ""
        self.first_operand = None
        self.operator = None
        return ""

    def backspace(self):
        self.current_value = self.current_value[:-1]
        return self.current_value

    def toggle_sign(self):
        if self.current_value and self.current_value[0] == '-':
            self.current_value = self.current_value[1:]
        elif self.current_value:
            self.current_value = '-' + self.current_value
        return self.current_value

    def add_decimal(self):
        if '.' not in self.current_value:
            if not self.current_value:
                self.current_value = '0.'
            else:
                self.current_value += '.'
        return self.current_value
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("错误：除数不能为零")
        return a / b

    def power(self, base, exponent):
        return math.pow(base, exponent)

    def square_root(self, x):
        if x < 0:
            raise ValueError("错误：不能对负数开平方")
        return math.sqrt(x)

    def cube_root(self, x):
        # 处理负数的情况
        if x < 0:
            return -math.pow(-x, 1/3)
        else:
            return math.pow(x, 1/3)

    def sin(self, angle, is_radian=False):
        if not is_radian:
            angle = math.radians(angle)
        return math.sin(angle)

    def cos(self, angle, is_radian=False):
        if not is_radian:
            angle = math.radians(angle)
        return math.cos(angle)

    def tan(self, angle, is_radian=False):
        if not is_radian:
            angle = math.radians(angle)
        return math.tan(angle)


class CalculatorApp(tk.Tk):
    def __init__(self, calculator):
        super().__init__()
        self.calculator = calculator
        self.title("简易计算器")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        # 设置字体支持中文显示
        self.style = ttk.Style()
        self.style.configure("TButton", font=("SimHei", 14))
        self.style.configure("TLabel", font=("SimHei", 20))
        # 自定义按钮样式
        self.style.configure("Number.TButton", background="#d0d0d0")
        self.style.configure("Operator.TButton", background="#ff9500", foreground="black")
        self.style.configure("Function.TButton", background="#5ac8fa")
        self.style.configure("Danger.TButton", background="#ff3b30", foreground="black")
        self.style.configure("Special.TButton", background="#a1caf1")
        # 悬停样式
        self.style.configure("Number.Hover.TButton", background="#b0b0b0")
        self.style.configure("Operator.Hover.TButton", background="#e68a00", foreground="white")
        self.style.configure("Function.Hover.TButton", background="#4db8e6")
        self.style.configure("Danger.Hover.TButton", background="#e6352a", foreground="white")
        self.style.configure("Special.Hover.TButton", background="#8db4d8")

        # 创建显示框
        self.display_var = tk.StringVar()
        # 算式显示区域
        self.expression_var = tk.StringVar()
        self.expression_display = ttk.Label(
            self, textvariable=self.expression_var, anchor="e",
            background="#f0f0f0", padding=(15, 5), font=("SimHei", 14)
        )
        self.expression_display.pack(fill=tk.BOTH, padx=10, pady=(5,2))

        self.display = ttk.Label(
            self, textvariable=self.display_var, anchor="e", background="#e8e8e8",
            padding=(15, 25), borderwidth=2, relief="solid", font=("SimHei", 24)
        )
        self.display.pack(fill=tk.BOTH, padx=10, pady=10)

        # 创建按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮布局
        # 添加角度单位切换按钮
        self.angle_unit_var = tk.StringVar(value="角度: 度")
        angle_unit_btn = ttk.Button(
            self, textvariable=self.angle_unit_var,
            command=lambda: self.angle_unit_var.set(f"角度: {self.calculator.toggle_angle_unit()[:3]}")
        )
        angle_unit_btn.pack(fill=tk.X, padx=10)

        buttons = [
            ('C', 0, 0, 2), ('⌫', 0, 2, 1), ('÷', 0, 3, 1),
            ('7', 1, 0, 1), ('8', 1, 1, 1), ('9', 1, 2, 1), ('×', 1, 3, 1),
            ('4', 2, 0, 1), ('5', 2, 1, 1), ('6', 2, 2, 1), ('-', 2, 3, 1),
            ('1', 3, 0, 1), ('2', 3, 1, 1), ('3', 3, 2, 1), ('+', 3, 3, 1),
            ('±', 4, 0, 1), ('0', 4, 1, 1), ('.', 4, 2, 1), ('=', 4, 3, 1),
            ('√', 5, 0, 1), ('∛', 5, 1, 1), ('^', 5, 2, 1), ('sin', 5, 3, 1),
            ('cos', 6, 0, 1), ('tan', 6, 1, 1), ('π', 6, 2, 1), ('清除', 6, 3, 1)
        ]

        # 创建按钮并放置
        for text, row, col, colspan in buttons:
            # 确定按钮样式
            style = "Number.TButton" if text.isdigit() or text == '.' else \
                    "Operator.TButton" if text in ['+', '-', '×', '÷', '^'] else \
                    "Function.TButton" if text in ['√', '∛', 'sin', 'cos', 'tan', 'π'] else \
                    "Danger.TButton" if text in ['C', '⌫', '清除'] else \
                    "Special.TButton" if text in ['±', '='] else "TButton"
            btn = ttk.Button(button_frame, text=text, command=lambda t=text: self.on_button_click(t), style=style)
            btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")
            # 添加悬停效果
            btn.bind('<Enter>', lambda e, b=btn, s=style: self.on_enter(e, b, s))
            btn.bind('<Leave>', lambda e, b=btn, s=style: self.on_leave(e, b, s))

        # 设置网格权重，使按钮可以扩展
        for i in range(7):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

        # 绑定键盘事件
        self.bind('<Key>', self.on_key_press)

    def on_enter(self, event, button, original_style):
        # 悬停时改变按钮样式
        if original_style == "Number.TButton":
            button.config(style="Number.Hover.TButton")
        elif original_style == "Operator.TButton":
            button.config(style="Operator.Hover.TButton")
        elif original_style == "Function.TButton":
            button.config(style="Function.Hover.TButton")
        elif original_style == "Danger.TButton":
            button.config(style="Danger.Hover.TButton")
        elif original_style == "Special.TButton":
            button.config(style="Special.Hover.TButton")

    def on_leave(self, event, button, original_style):
        # 离开时恢复按钮样式
        button.config(style=original_style)

    def on_key_press(self, event):
        # 处理键盘输入
        key = event.char
        if key.isdigit() or key == '.':
            self.on_button_click(key)
        elif key in ['+', '-', '*', '/', '^']:
            # 转换键盘符号为按钮符号
            symbol_map = {'*': '×', '/': '÷'}
            self.on_button_click(symbol_map.get(key, key))
        elif event.keysym in ['Return', 'Equal']:
            self.on_button_click('=')
        elif event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif event.keysym == 'p':
            self.on_button_click('π')

    def update_realtime_result(self):
        self.expression_var.set(self.calculator.get_current_expression())

    def on_button_click(self, text):
        try:
            prev_expression = self.calculator.get_current_expression()
            
            if text.isdigit():
                result = self.calculator.append_number(text)
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text == '.':
                result = self.calculator.add_decimal()
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text in ['+', '-', '×', '÷', '^', '√', '∛', 'sin', 'cos', 'tan']:
                self.calculator.set_operator(text)
                self.update_realtime_result()
            
            elif text == '=':
                result = self.calculator.calculate()
                current_expr = self.calculator.get_current_expression()
                self.display_var.set(result)
                self.expression_var.set(f"{current_expr} = {result}")
                self.calculator.expression = ''
                if result.startswith("错误:"):
                    messagebox.showerror("计算错误", result[4:])
                self.display_var.set(result)
                self.expression_var.set(f"{current_expr} = {result}")
            
            elif text == 'C':
                self.calculator.expression = ''
                result = self.calculator.clear()
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text == '⌫':
                result = self.calculator.backspace()
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text == '±':
                result = self.calculator.toggle_sign()
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text == 'π':
                result = self.calculator.append_number(math.pi)
                self.display_var.set(result)
                self.update_realtime_result()
            
            elif text == '清除':
                result = self.calculator.clear()
                self.display_var.set(result)
                self.update_realtime_result()

        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.display_var.set("错误")


if __name__ == "__main__":
    calc = Calculator()
    app = CalculatorApp(calc)
    app.mainloop()