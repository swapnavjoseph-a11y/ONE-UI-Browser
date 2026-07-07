import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView

class TrueOneUIBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("One UI Browser Hub")
        self.setGeometry(100, 100, 1100, 850)

        # 1. Premium Custom One UI Dark Theme Sheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000; /* Deep AMOLED Midnight Black */
            }
            QWidget#MainContainer {
                background-color: #000000;
            }
            /* One UI Welcome Header Text - CENTERED */
            QLabel#HeaderTitle {
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 28px;
                font-weight: bold;
                margin-top: 40px;
                margin-bottom: 5px;
            }
            QLabel#HeaderSubtitle {
                color: #8E8E93;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                margin-bottom: 30px;
            }
            /* Samsung-Style Massive Rounded Search Pill Bar */
            QLineEdit#SearchPill {
                background-color: #1C1C1E; /* Soft Dark Grey Card */
                border: 2px solid #1C1C1E;
                border-radius: 24px; /* Perfectly round pill corners */
                padding: 12px 24px;
                color: #FFFFFF; /* High contrast white text */
                font-size: 16px;
            }
            QLineEdit#SearchPill:focus {
                border: 2px solid #3F7DE8; /* Premium One UI Interactive Blue Accent */
                background-color: #222224;
            }
            /* Sleek Action Buttons */
            QPushButton[class="NavButton"] {
                background-color: #1C1C1E;
                border: none;
                border-radius: 18px; /* Beautiful squircle shape */
                min-width: 44px;
                min-height: 40px;
                color: #E3E3E3;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton[class="NavButton"]:hover {
                background-color: #2C2C2E;
                color: #FFFFFF;
            }
            /* One UI System Quick-Access App Shortcut Cards */
            QPushButton[class="WidgetCard"] {
                background-color: #1C1C1E;
                border: 1px solid #2C2C2E;
                border-radius: 20px; /* Rounded squircle cards */
                padding: 20px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 500;
                min-width: 130px;
                min-height: 90px;
            }
            QPushButton[class="WidgetCard"]:hover {
                background-color: #2C2C2E;
                border: 1px solid #3F7DE8; /* Subtle blue highlight outline */
            }
        """)

        # Core Stack Layout Structure
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.root_layout.setSpacing(15)

        # Create Top Navigation Panel
        self.nav_bar_layout = QHBoxLayout()
        self.nav_bar_layout.setSpacing(10)

        self.home_btn = QPushButton("🏠")
        self.home_btn.setProperty("class", "NavButton")
        self.back_btn = QPushButton("←")
        self.back_btn.setProperty("class", "NavButton")
        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setProperty("class", "NavButton")

        self.nav_bar_layout.addWidget(self.home_btn)
        self.nav_bar_layout.addWidget(self.back_btn)
        self.nav_bar_layout.addWidget(self.refresh_btn)
        self.nav_bar_layout.addStretch()

        # ==========================================
        # BUILD THE BRAND NEW CUSTOM ONE UI HUB VIEW
        # ==========================================
        self.hub_widget = QWidget()
        self.hub_layout = QVBoxLayout(self.hub_widget)
        self.hub_layout.setContentsMargins(50, 0, 50, 0)

        # Title block - Aligned to Center
        self.title_label = QLabel("Welcome to your UI")
        self.title_label.setObjectName("HeaderTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.subtitle_label = QLabel("Clean, custom dashboard workspace")
        self.subtitle_label.setObjectName("HeaderSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Huge central URL & Search Input Field Box
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchPill")
        self.search_bar.setPlaceholderText("Search Google or enter any website address...")

        # Interactive quick grid system row layout - CENTERED
        self.grid_layout = QHBoxLayout()
        self.grid_layout.setSpacing(20)

        self.card_google = QPushButton("🌐\nGoogle")
        self.card_google.setProperty("class", "WidgetCard")
        self.card_yt = QPushButton("📺\nYouTube")
        self.card_yt.setProperty("class", "WidgetCard")
        self.card_git = QPushButton("💻\nGitHub")
        self.card_git.setProperty("class", "WidgetCard")

        # MAGIC FIX: Add spacers to the left and right sides to squeeze the cards perfectly to the center
        self.grid_layout.addStretch()
        self.grid_layout.addWidget(self.card_google)
        self.grid_layout.addWidget(self.card_yt)
        self.grid_layout.addWidget(self.card_git)
        self.grid_layout.addStretch()

        # Mount items to the custom home view
        self.hub_layout.addStretch() # Push everything down slightly from the top bar
        self.hub_layout.addWidget(self.title_label)
        self.hub_layout.addWidget(self.subtitle_label)
        self.hub_layout.addWidget(self.search_bar)
        self.hub_layout.addSpacing(15)
        self.hub_layout.addLayout(self.grid_layout)
        self.hub_layout.addStretch() # Keep everything floating perfectly in the vertical center

        # Build Web View Screen Container Layer (Stays invisible until called)
        self.web_view = QWebEngineView()
        self.web_view.hide()

        # Wire Up User Click Interactions
        self.search_bar.returnPressed.connect(self.launch_web_routing)
        self.home_btn.clicked.connect(self.return_to_hub_dashboard)
        self.back_btn.clicked.connect(self.web_view.back)
        self.refresh_btn.clicked.connect(self.web_view.reload)

        # Connect Dashboard Cards to fire instantly
        self.card_google.clicked.connect(lambda: self.load_direct_link("https://google.com"))
        self.card_yt.clicked.connect(lambda: self.load_direct_link("https://youtube.com"))
        self.card_git.clicked.connect(lambda: self.load_direct_link("https://github.com"))

        # Put everything together inside the window frame
        self.root_layout.addLayout(self.nav_bar_layout)
        self.root_layout.addWidget(self.hub_widget)
        self.root_layout.addWidget(self.web_view)

        main_container = QWidget()
        main_container.setObjectName("MainContainer")
        main_container.setLayout(self.root_layout)
        self.setCentralWidget(main_container)

    def launch_web_routing(self):
        input_text = self.search_bar.text().strip()
        if not input_text:
            return

        if "." in input_text and " " not in input_text:
            if not input_text.startswith("http://") and not input_text.startswith("https://"):
                input_text = "https://" + input_text
            target_url = input_text
        else:
            query = input_text.replace(" ", "+")
            target_url = f"https://google.com/search?q={query}"

        self.load_direct_link(target_url)

    def load_direct_link(self, destination_url):
        self.hub_widget.hide()
        self.web_view.show()
        self.web_view.setUrl(QUrl(destination_url))

    def return_to_hub_dashboard(self):
        self.web_view.hide()
        self.search_bar.clear()
        self.hub_widget.show()

# Execution initialization point
app = QApplication(sys.argv)
window = TrueOneUIBrowser()
window.show()
sys.exit(app.exec())

