#!/usr/bin/env python3
"""Generate one-page resume PDF via PostScript → Ghostscript.
Format: Adam Pardonoff-inspired — centered, polished, single page.
Target: GM JR-202605769 ML Validation Engineer - Early Career.
"""

import subprocess, os

OUTPUT = os.path.join(os.path.dirname(__file__), "TaSain_Thomas_Resume.pdf")
PS = "/tmp/resume.ps"

# ── Layout constants (points, US Letter: 612 × 792) ──
PAGE_W = 612
MARGIN_L = 54   # ~0.75in
MARGIN_R = 54
TEXT_W = PAGE_W - MARGIN_L - MARGIN_R  # 504pt
CENTER = PAGE_W / 2
TOP = 720        # start below top edge
BOTTOM = 48      # minimum bottom margin
FONT = "Times-Roman"
FONT_B = "Times-Bold"
FONT_I = "Times-Italic"

# Tight spacing for one-page fit
LEADING = 11.2   # line spacing
SEC_GAP = 4      # gap after section header

y = TOP  # current vertical position (moves down; lower = closer to bottom)

def ps(s):
    f.write(s + "\n")

def emit_header():
    ps("%!PS-Adobe-3.0")
    ps("%%BoundingBox: 0 0 612 792")
    ps("%%Title: TaSain Thomas Resume")
    ps("%%Creator: generate_resume.py")
    ps("%%EndComments")
    ps("%%Page: 1 1")

def center_text(text, font_name, size, ypos):
    ps(f"/{font_name} findfont {size} scalefont setfont")
    ps(f"({text}) dup stringwidth pop 2 div neg {CENTER} add {ypos} moveto show")

def section_header(text):
    global y
    y -= 4  # space before rule
    ps("0.5 setlinewidth")
    ps(f"{MARGIN_L} {y} moveto {PAGE_W - MARGIN_R} {y} lineto stroke")
    y -= 6
    y -= LEADING
    center_text(text, FONT_B, 10.5, y)
    y -= 6
    ps(f"{MARGIN_L} {y} moveto {PAGE_W - MARGIN_R} {y} lineto stroke")
    y -= SEC_GAP

def gap(lines=1):
    global y
    y -= LEADING * lines

def make_pdf():
    global y, f
    with open(PS, "w") as f:
        emit_header()

        # ═══════════ NAME + CONTACT ═══════════
        y = TOP
        center_text("TaSain Thomas", FONT_B, 16, y)
        y -= 16
        # Contact line
        ps(f"/{FONT} findfont 9 scalefont setfont")
        contact = "(586) 873-0656  |  tasain@onwheelsdetailing.com  |  github.com/T-Thomas1  |  linkedin.com/in/tasain-thomas  |  tasainthomas.com"
        ps(f"({contact}) dup stringwidth pop 2 div neg {CENTER} add {y} moveto show")

        # pdfmark links for clickable contact items
        # GitHub
        ps("[/Rect [247 707 295 717] /Color [0 0 1] /Action << /Subtype /URI /URI (https://github.com/T-Thomas1) >> /Subtype /Link /ANN pdfmark")
        # LinkedIn
        ps("[/Rect [300 707 370 717] /Color [0 0 1] /Action << /Subtype /URI /URI (https://linkedin.com/in/tasain-thomas-539867249) >> /Subtype /Link /ANN pdfmark")
        # Portfolio
        ps("[/Rect [378 707 435 717] /Color [0 0 1] /Action << /Subtype /URI /URI (https://tasainthomas.com) >> /Subtype /Link /ANN pdfmark")
        # Email
        ps("[/Rect [145 707 255 717] /Color [0 0 1] /Action << /Subtype /URI /URI (mailto:tasain@onwheelsdetailing.com) >> /Subtype /Link /ANN pdfmark")

        gap(2)

        # ═══════════ EDUCATION ═══════════
        section_header("EDUCATION")

        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(Wayne State University) {MARGIN_L} {y} moveto show")
        ps(f"(Wayne State University) stringwidth pop {MARGIN_L} add /after_school exch def")
        ps(f"/{FONT} findfont 9.5 scalefont setfont")
        ps(f"(  \\267  B.S. Computer Science  |  May 2026  |  GPA: 3.4/4.0) after_school {y} moveto show")

        y -= LEADING
        ps(f"/{FONT_I} findfont 9 scalefont setfont")
        ps(f"(Trustworthy AI Coursework:) {MARGIN_L + 8} {y} moveto show")
        ps(f"(Trustworthy AI Coursework:) stringwidth pop {MARGIN_L + 8} add /after_cw exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(LoRA/QLoRA, RLHF/DPO/GRPO, Red Teaming, Machine Unlearning, Agentic AI Safety,) after_cw {y} moveto show")
        y -= LEADING
        ps(f"(Grounded VLMs, Chain-of-Thought Reasoning, HarmBench Benchmarking) {MARGIN_L + 8} {y} moveto show")
        gap(1)

        # ═══════════ CORE COMPETENCIES ═══════════
        section_header("CORE COMPETENCIES")
        y -= 2
        ps(f"/{FONT} findfont 9 scalefont setfont")
        comps1 = (
            "ML Validation  \\267  CI/CD  \\267  Red Teaming  \\267  Model Monitoring  \\267  "
            "LoRA/VLM Fine-Tuning  \\267  RAG  \\267  Simulation-Based Eval"
        )
        comps2 = (
            "Uncertainty Quantification  \\267  Kubernetes  \\267  Docker  \\267  "
            "Python  \\267  PyTorch  \\267  C++  \\267  Adversarial Robustness"
        )
        ps(f"({comps1}) {MARGIN_L + 4} {y} moveto show")
        y -= LEADING
        ps(f"({comps2}) {MARGIN_L + 4} {y} moveto show")
        gap(1)

        # ═══════════ PROFESSIONAL EXPERIENCE ═══════════
        section_header("PROFESSIONAL EXPERIENCE")

        # Magna — prominent
        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(Industry 4.0 / Automation Intern \\050Rotational\\051) {MARGIN_L} {y} moveto show")
        ps(f"(Industry 4.0 / Automation Intern \\050Rotational\\051) stringwidth pop {MARGIN_L} add /after_title exch def")
        ps(f"/{FONT_I} findfont 9.5 scalefont setfont")
        ps(f"( | Magna Electric Vehicle Structures) after_title {y} moveto show")
        ps(f"( | Magna Electric Vehicle Structures) stringwidth pop after_title add /after_co exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(  |  Sep 2023 \\267 Sep 2024) after_co {y} moveto show")

        magna_bullets = [
            "Delivered 4 automation projects on schedule by integrating real-time production data pipelines via custom API development",
            "Improved throughput 33% by implementing Vuforia Model Targets for vision-guided assembly verification on the manufacturing line",
            "Built C++/SQLite3 worker-to-station matching engine with evaluateFit() scoring algorithm, reducing assignment time 40% across production lines",
            "Reduced debug cycle time 25% by developing custom C# validation logic that automated error handling and root-cause identification",
        ]
        for b in magna_bullets:
            y -= LEADING
            ps(f"/{FONT} findfont 9 scalefont setfont")
            ps(f"(\\267  {b}) {MARGIN_L + 8} {y} moveto show")

        gap(0)

        # BlueMind — condensed to one line
        y -= LEADING
        ps(f"/{FONT_B} findfont 9.5 scalefont setfont")
        ps(f"(Registered Behavior Technician) {MARGIN_L} {y} moveto show")
        ps(f"(Registered Behavior Technician) stringwidth pop {MARGIN_L} add /after_bm exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"( | BlueMind Therapy LLC  |  Sep 2024 \\267 Present) after_bm {y} moveto show")
        gap(1)

        # ═══════════ ENGINEERING PROJECTS ═══════════
        section_header("ENGINEERING PROJECTS")

        # Project 1: BMI Estimation
        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(ML Validation Pipeline: BMI Estimation from Images) {MARGIN_L} {y} moveto show")
        ps(f"(ML Validation Pipeline: BMI Estimation from Images) stringwidth pop {MARGIN_L} add /after_p1 exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(  |  github.com/T-Thomas1  |  Apr 2026) after_p1 {y} moveto show")

        bmi_bullets = [
            "Built secure VLM evaluation pipeline achieving 89% accuracy (MAE 1.24) via LoRA fine-tuning of 7B vision-language model, reducing training cost 95% vs. full fine-tuning",
            "Implemented privacy-preserving validation layers (face blurring, synthetic data via BEDLAM) and LLM-as-Judge quality gates, cutting hallucination and refusal rates 40%",
            "Integrated chain-of-thought reasoning with zero-trust validation, benchmarking safety against HarmBench standards for adversarial robustness",
        ]
        for b in bmi_bullets:
            y -= LEADING
            ps(f"/{FONT} findfont 9 scalefont setfont")
            ps(f"(\\267  {b}) {MARGIN_L + 8} {y} moveto show")
        gap(1)

        # Project 2: MLOps
        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(MLOps Infrastructure \\046 AI Agent Engineering) {MARGIN_L} {y} moveto show")
        ps(f"(MLOps Infrastructure \\046 AI Agent Engineering) stringwidth pop {MARGIN_L} add /after_p2 exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(  |  Mar 2026 \\267 Present) after_p2 {y} moveto show")

        mlops_bullets = [
            "Architected auto-scaling Kubernetes inference cluster with GPU passthrough serving LLMs at 99.9% uptime, integrating model monitoring and real-time incident response",
            "Embedded red-team security testing (Kali Linux) into CI/CD, patching prompt injection vulnerabilities pre-production and hardening deployment pipelines",
        ]
        for b in mlops_bullets:
            y -= LEADING
            ps(f"/{FONT} findfont 9 scalefont setfont")
            ps(f"(\\267  {b}) {MARGIN_L + 8} {y} moveto show")
        gap(1)

        # Project 3: CRM
        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(SaaS Booking \\046 Payment Platform) {MARGIN_L} {y} moveto show")
        ps(f"(SaaS Booking \\046 Payment Platform) stringwidth pop {MARGIN_L} add /after_p3 exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"( | github.com/T-Thomas1/on-wheels_detailing-crm) after_p3 {y} moveto show")

        y -= LEADING
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(\\267  Engineered full-stack CRM (Python/JavaScript) with Stripe payments and Telegram Bot API; deployed on DigitalOcean with Nginx, systemd, and Cloudflare CI/CD at 24/7 uptime) {MARGIN_L + 8} {y} moveto show")
        gap(1)

        # Project 4: Mobile Capstone — condensed
        y -= 2
        ps(f"/{FONT_B} findfont 10 scalefont setfont")
        ps(f"(Real-Time Mobile Collaboration Platform) {MARGIN_L} {y} moveto show")
        ps(f"(Real-Time Mobile Collaboration Platform) stringwidth pop {MARGIN_L} add /after_p4 exch def")
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"( | Capstone  |  May 2026) after_p4 {y} moveto show")

        y -= LEADING
        ps(f"/{FONT} findfont 9 scalefont setfont")
        ps(f"(\\267  Developed cross-platform \\050Flutter/Dart\\051 collaborative workspace integrating ZegoCloud real-time video and RevenueCat subscription monetization; shipped to production for client deployment) {MARGIN_L + 8} {y} moveto show")
        gap(1)

        # ═══════════ TECHNICAL SKILLS ═══════════
        section_header("TECHNICAL SKILLS")

        skills = [
            ("Languages:", "Python, C++, JavaScript, SQL, Java, Dart"),
            ("ML / AI:", "PyTorch, TensorFlow, Hugging Face, LangChain, LoRA/QLoRA, RAG, Vector Databases, Transformer Architectures"),
            ("MLOps:", "Kubernetes, Docker, CI/CD, Model Serving \\046 Monitoring, Helm, Terraform, GPU Passthrough"),
            ("Cloud \\046 Infra:", "AWS/Azure, DigitalOcean, Nginx, Cloudflare, Proxmox, systemd"),
            ("Security:", "Red Teaming, Prompt Injection Defense, Zero Trust, Adversarial Robustness, Kali Linux"),
        ]
        for label, content in skills:
            y -= LEADING
            ps(f"/{FONT_B} findfont 9 scalefont setfont")
            ps(f"({label}) {MARGIN_L + 4} {y} moveto show")
            ps(f"({label}) stringwidth pop {MARGIN_L + 4} add /after_lbl exch def")
            ps(f"/{FONT} findfont 9 scalefont setfont")
            ps(f"(  {content}) after_lbl {y} moveto show")

        # ═══════════ FOOTER ═══════════
        ps("showpage")
        ps("%%EOF")

    # Convert to PDF
    subprocess.run([
        "gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-q",
        "-sOutputFile=" + OUTPUT, PS
    ], check=True)

    # Verify
    result = subprocess.run([
        "gs", "-sDEVICE=txtwrite", "-dNOPAUSE", "-dBATCH", "-q",
        "-sOutputFile=/tmp/verify.txt", OUTPUT
    ], capture_output=True, text=True)
    with open("/tmp/verify.txt") as vf:
        text = vf.read()
    print("--- VERIFICATION ---")
    print(f"File: {OUTPUT}")
    print(f"Size: {os.path.getsize(OUTPUT)} bytes")
    print(f"First 800 chars:")
    print(text[:800])
    print("...")

if __name__ == "__main__":
    make_pdf()
