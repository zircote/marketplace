# NSIP Discover Demo
# Demonstrates the /nsip:lookup command with a real LPN ID

Output demos/nsip-discover.gif

Set Shell "bash"
Set Theme "Dracula"
Set FontSize 14
Set Width 900
Set Height 500
Set TypingSpeed 50ms

Type "# NSIP Plugin - Animal Lookup"
Enter
Sleep 500ms

Type "claude  --dangerously-skip-permissions '/nsip:lookup 6401492025FLE087'"
Enter
Sleep 90s

Type "# Returns breeding values, lineage, and trait data"
Enter
Sleep 5s
