import ast
import operator

# Allowed binary operators
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators (+x, -x)
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr: str):
    """Safely evaluate math expressions with +, -, *, /, %, ** and parentheses."""
    tree = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in BIN_OPS:
                raise ValueError("Operator mojaz nist!")
            left = _eval(node.left)
            right = _eval(node.right)
            if op_type in (ast.Div, ast.Mod) and right == 0:
                raise ZeroDivisionError("Taghsim bar sefr emkan pazir nist!")
            return BIN_OPS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in UNARY_OPS:
                raise ValueError("Alamat ghabl az adad mojaz nist!")
            return UNARY_OPS[op_type](_eval(node.operand))
        else:
            raise ValueError("Ebarat riazi na-moatabar ast!")

    return _eval(tree)


def format_num(val):
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    if isinstance(val, float):
        return f"{val:.6g}"
    return str(val)


def print_banner():
    print("=" * 56)
    print("   KHOSH AMADID BE MASHIN HESAB ")
    print("=" * 56)
    print("Amalgarha: +  -  *  /  % (baghimandeh)  ** (tavan)  ( )")
    print("Mesal: ((10 + 5) * 2) ** 2 % 7")
    print("-" * 56)
    print("Dastoorat-e komaki:")
    print("  prev  ya  !prev  -> Avardane javab-e mohasebe-ye ghabli")
    print("  !<shomare>       -> Avardane javab-e yek item az tarikhche (masalan !1)")
    print("  history          -> Didane list-e tarikhche-ye mohasebat")
    print("  clear_hist       -> Pak kardane tarikhche")
    print("  help             -> Namayesh-e dobare-ye rahnamayi")
    print("  exit  ya  quit   -> Khorooj az barname")
    print("=" * 56)


def main():
    history = []  # List of tuples: (expression, result)
    print_banner()

    while True:
        try:
            user_input = input("\nEbarat ya dastoor ra vared konid > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKhodafez! Movafagh bashid.")
            break

        if not user_input:
            print("Lotfan yek ebarat-e riazi ya dastoor vared konid.")
            continue

        cmd = user_input.lower()

        if cmd in ("exit", "quit"):
            print("Mamnoon ke az mashin hesab estefade kardid. Khodafez!")
            break

        if cmd == "help":
            print_banner()
            continue

        if cmd == "clear_hist":
            history.clear()
            print("Tarikhche ba movafaghiat pak shod.")
            continue

        if cmd == "history":
            if not history:
                print("Hanuz hich mohasebei dar tarikhche sabt nashode ast.")
            else:
                print("\n--- Tarikhche-ye Mohasebat ---")
                for idx, (expr_str, res_val) in enumerate(history, start=1):
                    print(f"  [{idx}] {expr_str} = {format_num(res_val)}")
            continue

        # Recall previous calculation result
        if cmd in ("prev", "!prev"):
            if not history:
                print("Mohasebe-ye ghabli vojud nadarad! Avval yek ebarat hesab konid.")
            else:
                last_expr, last_res = history[-1]
                print(f"Mohasebe-ye ghabli: {last_expr} = {format_num(last_res)}")
                print(f"Meghdar-e amade baraye estefade: {format_num(last_res)}")
            continue

        # Recall specific history item by index, e.g. !1 or !2
        if user_input.startswith("!") and user_input[1:].isdigit():
            idx = int(user_input[1:])
            if 1 <= idx <= len(history):
                sel_expr, sel_res = history[idx - 1]
                print(f"Item [{idx}]: {sel_expr} = {format_num(sel_res)}")
                print(f"Meghdar-e amade baraye estefade: {format_num(sel_res)}")
            else:
                print(f"Shomare-ye [{idx}] dar tarikhche vojud nadarad.")
            continue

        # Support replacing 'prev' or '!prev' inside a new expression, e.g. "prev * 10"
        expr_to_eval = user_input
        if "prev" in cmd and history:
            last_res_str = format_num(history[-1][1])
            expr_to_eval = (
                expr_to_eval.replace("!prev", f"({last_res_str})")
                .replace("PREV", f"({last_res_str})")
                .replace("prev", f"({last_res_str})")
            )

        try:
            result = safe_eval(expr_to_eval)
            history.append((expr_to_eval, result))
            print(f"Natije: {format_num(result)}")
        except ZeroDivisionError as e:
            print(f"Khata: {e}")
        except SyntaxError:
            print("Khata: Sakhtar-e ebarat eshtebah ast! Parantezha va amalgarha ra check konid.")
        except ValueError as e:
            print(f"Khata: {e}")
        except Exception as e:
            print(f"Khata-ye gheyr-e montazere: {e}")


if __name__ == "__main__":
    main()
import ast
import operator

# Allowed binary operators
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators (+x, -x)
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr: str):
    """Safely evaluate math expressions with +, -, *, /, %, ** and parentheses."""
    tree = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in BIN_OPS:
                raise ValueError("Operator mojaz nist!")
            left = _eval(node.left)
            right = _eval(node.right)
            if op_type in (ast.Div, ast.Mod) and right == 0:
                raise ZeroDivisionError("Taghsim bar sefr emkan pazir nist!")
            return BIN_OPS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in UNARY_OPS:
                raise ValueError("Alamat ghabl az adad mojaz nist!")
            return UNARY_OPS[op_type](_eval(node.operand))
        else:
            raise ValueError("Ebarat riazi na-moatabar ast!")

    return _eval(tree)


def format_num(val):
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    if isinstance(val, float):
        return f"{val:.6g}"
    return str(val)


def print_banner():
    print("=" * 56)
    print("   KHOSH AMADID BE MASHIN HESAB TERMINAL (PYTHON)")
    print("=" * 56)
    print("Amalgarha: +  -  *  /  % (baghimandeh)  ** (tavan)  ( )")
    print("Mesal: ((10 + 5) * 2) ** 2 % 7")
    print("-" * 56)
    print("Dastoorat-e komaki:")
    print("  prev  ya  !prev  -> Avardane javab-e mohasebe-ye ghabli")
    print("  !<shomare>       -> Avardane javab-e yek item az tarikhche (masalan !1)")
    print("  history          -> Didane list-e tarikhche-ye mohasebat")
    print("  clear_hist       -> Pak kardane tarikhche")
    print("  help             -> Namayesh-e dobare-ye rahnamayi")
    print("  exit  ya  quit   -> Khorooj az barname")
    print("=" * 56)


def main():
    history = []  # List of tuples: (expression, result)
    print_banner()

    while True:
        try:
            user_input = input("\nEbarat ya dastoor ra vared konid > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKhodafez! Movafagh bashid.")
            break

        if not user_input:
            print("Lotfan yek ebarat-e riazi ya dastoor vared konid.")
            continue

        cmd = user_input.lower()

        if cmd in ("exit", "quit"):
            print("Mamnoon ke az mashin hesab estefade kardid. Khodafez!")
            break

        if cmd == "help":
            print_banner()
            continue

        if cmd == "clear_hist":
            history.clear()
            print("Tarikhche ba movafaghiat pak shod.")
            continue

        if cmd == "history":
            if not history:
                print("Hanuz hich mohasebei dar tarikhche sabt nashode ast.")
            else:
                print("\n--- Tarikhche-ye Mohasebat ---")
                for idx, (expr_str, res_val) in enumerate(history, start=1):
                    print(f"  [{idx}] {expr_str} = {format_num(res_val)}")
            continue

        # Recall previous calculation result
        if cmd in ("prev", "!prev"):
            if not history:
                print("Mohasebe-ye ghabli vojud nadarad! Avval yek ebarat hesab konid.")
            else:
                last_expr, last_res = history[-1]
                print(f"Mohasebe-ye ghabli: {last_expr} = {format_num(last_res)}")
                print(f"Meghdar-e amade baraye estefade: {format_num(last_res)}")
            continue

        # Recall specific history item by index, e.g. !1 or !2
        if user_input.startswith("!") and user_input[1:].isdigit():
            idx = int(user_input[1:])
            if 1 <= idx <= len(history):
                sel_expr, sel_res = history[idx - 1]
                print(f"Item [{idx}]: {sel_expr} = {format_num(sel_res)}")
                print(f"Meghdar-e amade baraye estefade: {format_num(sel_res)}")
            else:
                print(f"Shomare-ye [{idx}] dar tarikhche vojud nadarad.")
            continue

        # Support replacing 'prev' or '!prev' inside a new expression, e.g. "prev * 10"
        expr_to_eval = user_input
        if "prev" in cmd and history:
            last_res_str = format_num(history[-1][1])
            expr_to_eval = (
                expr_to_eval.replace("!prev", f"({last_res_str})")
                .replace("PREV", f"({last_res_str})")
                .replace("prev", f"({last_res_str})")
            )

        try:
            result = safe_eval(expr_to_eval)
            history.append((expr_to_eval, result))
            print(f"Natije: {format_num(result)}")
        except ZeroDivisionError as e:
            print(f"Khata: {e}")
        except SyntaxError:
            print("Khata: Sakhtar-e ebarat eshtebah ast! Parantezha va amalgarha ra check konid.")
        except ValueError as e:
            print(f"Khata: {e}")
        except Exception as e:
            print(f"Khata-ye gheyr-e montazere: {e}")


if __name__ == "__main__":
    main()
