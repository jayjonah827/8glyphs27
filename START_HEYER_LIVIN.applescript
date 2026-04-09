-- START HEYER LIVIN
-- Double-click this in Script Editor, then File > Export > Application
-- to turn it into a double-clickable app.
-- This opens your entire workspace in one move.

set glyph8Path to (path to home folder as string) & "Desktop:Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files:03_RESEARCH:GLYPH8:"
set legalPath to (path to home folder as string) & "Desktop:Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files:04_LEGAL:Housing:"
set researchPath to (path to home folder as string) & "Desktop:Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files:03_RESEARCH:"
set creativePath to (path to home folder as string) & "Desktop:Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files:06_CREATIVE:"

-- Open Finder windows for your key folders
tell application "Finder"
	activate
	-- Open the main Heyer Livin folder
	open folder ((path to home folder as string) & "Desktop:Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files:")
end tell

-- Open Terminal and launch GLYPH-8
tell application "Terminal"
	activate
	do script "cd ~/Desktop/'Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files'/03_RESEARCH/GLYPH8 && python3 glyph8.py"
end tell

-- Display startup message
display dialog "HEYER LIVIN SYSTEM ACTIVE

GLYPH-8 running in Terminal
Folders open in Finder

Today: " & (do shell script "date '+%A, %B %d %Y'") & "

Legal answer due: April 3, 2026" buttons {"Let's work"} default button 1 with title "GLYPH-8"
