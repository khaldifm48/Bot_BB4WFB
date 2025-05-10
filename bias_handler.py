def load_weekly_bias(file_path="weekly_bias.txt"):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        bias = None
        context = None

        for line in lines:
            if line.startswith("bias:"):
                bias = line.split(":")[1].strip().lower()
            elif line.startswith("context:"):
                context = line.split(":")[1].strip().lower()

        if bias not in ["bullish", "bearish", "neutral"]:
            raise ValueError("⚠️ bias يجب أن يكون bullish أو bearish أو neutral")

        if context not in ["expansion", "consolidation", "reversal"]:
            raise ValueError("⚠️ context يجب أن يكون expansion أو consolidation أو reversal")

        print(f"📘 Weekly Bias: {bias.upper()} | Context: {context.upper()}")
        return bias, context

    except Exception as e:
        print(f"❌ خطأ أثناء قراءة ملف الانحياز: {e}")
        return None, None

if __name__ == "__main__":
    load_weekly_bias()

