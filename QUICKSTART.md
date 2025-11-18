# Quick Start Guide

This guide will help you get started with the UI/UX Bug Detection & Fixing Evaluation Project in under 5 minutes.

## ⚡ Fastest Path (3 Steps)

### Step 1: Install Dependencies (1 minute)

```bash
pip install pytest playwright pytest-playwright
playwright install chromium
```

### Step 2: Run Buggy App (30 seconds)

```bash
cd buggy-app
python -m http.server 8080
```

Open http://localhost:8080 - Notice the bugs! 🐛

### Step 3: Run Tests (1 minute)

Open a new terminal:

```bash
pytest tests/test_ui.py -v
```

See test failures showing bugs detected ❌

---

## 🎯 What to Look For

### In the Buggy App (http://localhost:8080)

When you open the buggy app, you should see:

1. **Navigation overlaps the content** (left side)
2. **Only ONE task card visible** (others hidden underneath)
3. **No "Add Task" button** (it's hidden!)
4. **Markdown looks weird** (plain text, no formatting)
5. **Footer may cover content** (scroll down)

### In the Test Output

```
FAILED test_ui.py::test_no_task_cards_overlap
FAILED test_ui.py::test_submit_button_visible
FAILED test_ui.py::test_headers_rendered_as_html
...
```

These failures confirm bugs are detected! ✅

---

## 🔧 Try the Fixed Version

### Stop the buggy app (Ctrl+C), then:

```bash
cd ../fixed-app
python -m http.server 8080
```

### Run tests again:

```bash
pytest tests/test_ui.py -v
```

### You should see:

```
PASSED test_ui.py::test_no_task_cards_overlap ✅
PASSED test_ui.py::test_submit_button_visible ✅
PASSED test_ui.py::test_headers_rendered_as_html ✅
...
===================== 25 passed in 15.2s =====================
```

All tests pass! 🎉

---

## 📖 Next Steps

1. **Compare the code:**
   - Look at `buggy-app/styles.css` vs `fixed-app/styles.css`
   - Check `buggy-app/app.js` vs `fixed-app/app.js`

2. **Read the analysis:**
   - `BUG_IDENTIFICATION.md` - See all 15 bugs explained
   - `EVALUATION_REPORT.md` - Full evaluation

3. **Explore the tests:**
   - `tests/test_ui.py` - See how bugs are detected

---

## 🐳 Docker Alternative (One Command)

### Buggy Version:
```bash
cd buggy-app
docker build -t task-manager-buggy . && docker run -p 8080:8080 task-manager-buggy
```

### Fixed Version:
```bash
cd fixed-app
docker build -t task-manager-fixed . && docker run -p 8080:8080 task-manager-fixed
```

---

## 🆘 Troubleshooting

### Port 8080 already in use?

```bash
# Use a different port
python -m http.server 3000

# Update test command
pytest tests/test_ui.py --app-url=http://localhost:3000 -v
```

### Playwright not working?

```bash
# Reinstall Playwright
pip install playwright --force-reinstall
playwright install chromium
```

### Tests failing on fixed app?

Make sure you:
1. Stopped the buggy app server
2. Started the fixed app server
3. Waiting for server to be ready (http://localhost:8080 loads)

---

## 🎓 What You'll Learn

By exploring this project, you'll understand:

- ✅ Common CSS layout bugs (absolute positioning issues)
- ✅ JavaScript rendering problems
- ✅ How to write UI tests with Playwright
- ✅ Systematic bug detection and fixing
- ✅ Best practices for web development

---

## 📊 Quick Stats

- **Bugs Created:** 15
- **Bugs Fixed:** 15
- **Test Cases:** 25+
- **Time to Complete:** ~5 minutes
- **Success Rate:** 100%

---

## 🎯 Challenge Yourself

Try to:
1. Find all 15 bugs without looking at `BUG_IDENTIFICATION.md`
2. Fix them yourself before checking `fixed-app/`
3. Write additional test cases
4. Add new features (dark mode, filters, etc.)

---

**Ready? Start with Step 1 above! 🚀**
