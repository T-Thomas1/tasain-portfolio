#!/usr/bin/env python3
"""One-page resume PDF via PostScript → Ghostscript. No rules, text-wrapped, centered layout."""
import subprocess, os

OUTPUT = os.path.join(os.path.dirname(__file__), "TaSain_Thomas_Resume.pdf")
PS = "/tmp/resume.ps"

PAGE_W, MARGIN_L, MARGIN_R = 612, 48, 48
TEXT_W = PAGE_W - MARGIN_L - MARGIN_R  # 516pt
CENTER = PAGE_W / 2
TOP, BOTTOM = 732, 40
FONT, FONT_B, FONT_I = "Times-Roman", "Times-Bold", "Times-Italic"
LEADING = 11.0

# ── char budget per line at given pt size (conservative) ──
# Times-Roman ~4.3pt/char at 9pt → 516/4.3 ≈ 120. Use 100 for safety.
def max_chars(size):
    return int(TEXT_W / (size * 0.48))  # ~100 at 9pt, ~92 at 10pt

y = TOP

def ps(s):
    f.write(s + "\n")

def font(name, size):
    ps(f"/{name} findfont {size} scalefont setfont")

def show(text, x, ypos, fname, fsize):
    font(fname, fsize)
    ps(f"({text}) {x} {ypos} moveto show")

def center(text, fname, fsize, ypos):
    font(fname, fsize)
    ps(f"({text}) dup stringwidth pop 2 div neg {CENTER} add {ypos} moveto show")

def lines(text, x, fname, fsize, budget=None):
    """Emit wrapped lines at current y, advancing y. Returns number of lines emitted."""
    global y
    if budget is None:
        budget = max_chars(fsize)
    words = text.split()
    cur = ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if len(test) > budget and cur:
            y -= LEADING
            show(cur, x, y, fname, fsize)
            cur = w
        else:
            cur = test
    if cur:
        y -= LEADING
        show(cur, x, y, fname, fsize)

def section(title):
    global y
    y -= LEADING * 0.5
    center(title, FONT_B, 10, y)
    y -= LEADING * 0.8

def rule():
    global y
    y -= 2

def gap(n=1):
    global y
    y -= LEADING * n

def title_line(bold_part, italic_part, date_part, fsize=9.5):
    """Role | Company | Date — inline, wraps if too long."""
    global y
    y -= LEADING
    font(FONT_B, fsize)
    ps(f"({bold_part}) {MARGIN_L} {y} moveto show")
    ps(f"({bold_part}) stringwidth pop {MARGIN_L} add /tx exch def")
    if italic_part:
        font(FONT_I, fsize)
        ps(f"({italic_part}) tx {y} moveto show")
        ps(f"({italic_part}) stringwidth pop tx add /tx exch def")
    if date_part:
        font(FONT, max(fsize - 0.5, 8))
        ps(f"({date_part}) tx {y} moveto show")

def bullet(text, fsize=8.7):
    lines("  \267  " + text, MARGIN_L, FONT, fsize)

def make_pdf():
    global y, f
    with open(PS, "w") as f:
        ps("%!PS-Adobe-3.0")
        ps("%%BoundingBox: 0 0 612 792")
        ps("%%Title: TaSain Thomas Resume")
        ps("%%Page: 1 1")

        # ── NAME ──
        y = TOP
        center("TaSain Thomas", FONT_B, 15, y)

        # ── CONTACT (2 lines) ──
        y -= 18
        center("tasainthomas1@gmail.com  |  (586) 873-0656  |  Detroit, MI", FONT, 8.5, y)
        y -= 12
        center("github.com/T-Thomas1  |  linkedin.com/in/tasain-thomas  |  tasainthomas.com", FONT, 8.5, y)
        gap(1)

        # ── EDUCATION ──
        section("EDUCATION")
        y -= 2
        title_line("Wayne State University", None, "  B.S. Computer Science  |  May 2026  |  GPA: 3.4/4.0", 9.5)
        lines("Trustworthy AI Coursework: LoRA/QLoRA, RLHF/DPO/GRPO, Red Teaming, Machine Unlearning, Agentic AI Safety, Grounded VLMs, Chain-of-Thought Reasoning, HarmBench Benchmarking", MARGIN_L + 8, FONT, 8.7, 105)
        gap(1)

        # ── CORE COMPETENCIES ──
        section("CORE COMPETENCIES")
        y -= 2
        lines("ML Validation  \267  CI/CD  \267  Red Teaming  \267  Model Monitoring  \267  LoRA/VLM Fine-Tuning  \267  RAG  \267  Simulation-Based Evaluation  \267  Uncertainty Quantification  \267  Kubernetes  \267  Docker  \267  Python  \267  PyTorch  \267  C++  \267  Adversarial Robustness", MARGIN_L, FONT, 8.7, 105)
        gap(1)

        # ── PROFESSIONAL EXPERIENCE ──
        section("PROFESSIONAL EXPERIENCE")

        # Magna
        y -= 2
        title_line("Industry 4.0 / Automation Intern (Rotational)", " | Magna EV Structures", "  |  Sep 2023 \267 Sep 2024")
        magna = [
            "Delivered 4 automation projects on schedule by integrating real-time production data pipelines via custom API development",
            "Improved throughput 33% by implementing Vuforia Model Targets for vision-guided assembly verification",
            "Built C++/SQLite3 worker-to-station matching engine with evaluateFit() scoring algorithm, reducing assignment time 40%",
            "Reduced debug cycle time 25% by developing custom C# validation logic that automated error handling and root-cause identification",
        ]
        for b in magna:
            bullet(b)

        # BlueMind
        gap(0.3)
        title_line("Registered Behavior Technician", " | BlueMind Therapy LLC", "  |  Sep 2024 \267 Present", 9)
        gap(1)

        # ── ENGINEERING PROJECTS ──
        section("ENGINEERING PROJECTS")

        # BMI
        y -= 2
        title_line("BMI Estimator with Reasoning: Conformal Prediction + GPT-as-Judge", None, "  |  Apr 2026")
        bullet("Trained a Squeeze-and-Excitation DenseNet (SE-DenseNet121) in PyTorch on Celeb-FBI (7,208 images), achieving 2.81 BMI-point MAE (11.56% MAPE)")
        bullet("Added split conformal prediction for calibrated uncertainty: 90% intervals with 90.4% verified coverage on held-out data")
        bullet("Layered a GPT-4.1-Nano LLM-as-judge reasoning module that explains each estimate and flags edge cases")
        gap(0.8)

        # MLOps
        title_line("MLOps Infrastructure & AI Agent Engineering", None, "  |  Mar 2026 \267 Present")
        bullet("Architected auto-scaling Kubernetes inference cluster with GPU passthrough serving LLMs at 99.9% uptime, with model monitoring and real-time incident response")
        bullet("Embedded red-team security testing (Kali Linux) into CI/CD, patching prompt injection vulnerabilities pre-production")
        gap(0.8)

        # CRM
        title_line("SaaS Booking & Payment Platform", None, "  |  github.com/T-Thomas1/on-wheels_detailing-crm")
        bullet("Engineered full-stack CRM (Python/JavaScript) with Stripe payments and Telegram Bot API; deployed on DigitalOcean, Nginx, systemd, Cloudflare CI/CD at 24/7 uptime")
        gap(0.8)

        # Mobile
        title_line("Real-Time Mobile Collaboration Platform", None, "  |  Capstone, May 2026")
        bullet("Developed cross-platform (Flutter/Dart) collaborative workspace integrating ZegoCloud real-time video and RevenueCat subscription monetization; shipped to production for client deployment")
        gap(1)

        # ── TECHNICAL SKILLS ──
        section("TECHNICAL SKILLS")
        y -= 2
        for label, content in [
            ("Languages:", "Python, C++, JavaScript, SQL, Java, Dart"),
            ("ML / AI:", "PyTorch, TensorFlow, Hugging Face, LangChain, LoRA/QLoRA, RAG, Vector Databases, Transformer Architectures"),
            ("MLOps:", "Kubernetes, Docker, CI/CD, Model Serving & Monitoring, Helm, Terraform, GPU Passthrough"),
            ("Cloud / Infra:", "AWS/Azure, DigitalOcean, Nginx, Cloudflare, Proxmox, systemd"),
            ("Security:", "Red Teaming, Prompt Injection Defense, Zero Trust, Adversarial Robustness, Kali Linux"),
        ]:
            y -= LEADING
            font(FONT_B, 8.7)
            ps(f"({label}) {MARGIN_L} {y} moveto show")
            ps(f"({label}) stringwidth pop {MARGIN_L} add /tl exch def")
            font(FONT, 8.7)
            ps(f"(  {content}) tl {y} moveto show")

        ps("showpage")
        ps("%%EOF")

    # Build PDF
    subprocess.run(["gs","-sDEVICE=pdfwrite","-dNOPAUSE","-dBATCH","-q",
                    "-sOutputFile="+OUTPUT, PS], check=True)

    # Verify
    subprocess.run(["gs","-sDEVICE=txtwrite","-dNOPAUSE","-dBATCH","-q",
                    "-sOutputFile=/tmp/verify.txt", OUTPUT], check=True)
    text = open("/tmp/verify.txt").read()
    pages = text.count("\f") + 1
    print(f"Pages: {pages}  |  Size: {os.path.getsize(OUTPUT)} bytes")
    if pages > 1:
        print("WARNING: OVERFLOW TO PAGE 2")
    print("---")
    print(text[:1000])

if __name__ == "__main__":
    make_pdf()
