# Dashboard UI Modification Plan

## Task: Modify Dashboard UI

### Information Gathered
- **Current File Structure:**
  - `frontend/dashboard.html` - Main dashboard page with Quick Actions section
  - `frontend/styles.css` - Global styles with CSS variables for theming
  
- **Key Findings:**
  - The "Ask AI" button is currently in `.action-grid` section (line ~58)
  - Brand colors: `--brand: #0f766e` and `--brand-strong: #0b5e57`
  - There's a sidebar that shifts content on desktop (`margin-left: 240px`)
  - Responsive breakpoints at 768px and 480px

### Plan

#### Step 1: Edit dashboard.html
- **Remove**: "Ask AI" button from Quick Actions grid
  ```html
  <!-- REMOVE THIS LINE -->
  <button class="btn" onclick="window.location='ai_assistant.html'">Ask AI</button>
  ```
- **Add**: Fixed "Ask AI" button at top-right corner before `.container` div
  ```html
  <a href="ai_assistant.html" class="ai-floating-btn" title="Ask AI Assistant">🤖</a>
  ```

#### Step 2: Edit styles.css
- **Add**: New CSS rules for `.ai-floating-btn`
  - Fixed position: top-right corner
  - Modern rounded design (circular or pill shape)
  - Match brand colors
  - Hover effects
  - Responsive: adjust position on mobile

### Dependent Files to be Edited
- `frontend/dashboard.html` - Remove old button, add new fixed button
- `frontend/styles.css` - Add new CSS class for floating button

### Followup Steps
- Task complete after editing both files
- No installation or testing required as this is static HTML/CSS modification

---

**Confirmation Required from User Before Proceeding**
