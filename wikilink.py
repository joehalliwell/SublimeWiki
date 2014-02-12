import sublime, sublime_plugin, os, re

class WikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):        
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        #find the cursor
        location = self.view.sel()[0]
        
        # find the link text under the cursor
        link = self.view.substr(self.view.extract_scope(location.a))
        
        if "link" not in self.view.scope_name(location.a):
            sublime.status_message("Can only handle links!")
            return
        if "title" in self.view.scope_name(location.a):
            sublime.status_message("Can't handle link titles!")
            return

        # TODO: Make a safe filename

        # TODO: Special cases for 
        #sublime.status_message("try to open " + link)
        #sublime.active_window().run_command('open_url', {"url": link})
        #sublime.status_message("try to mail " + link)
        #sublime.active_window().run_command('open_url', {"url": "mailto:"+link})
        
        #okay, we're good. Keep on keepin' on.        
        
        #compile the full file name and path.
        new_file = os.path.join(directory, link + ".wiki")

        #debug section: uncomment to write to the console
        # print("Location: %d" % location.a)
        # print("Selected word is '%s'" % word)
        # print("Full file path: %s" % new_file)
        # print("Selected word link is '%s'" % self.view.scope_name(location.a))
        # if internalLink in self.view.scope_name(location.a):
        #     print("this is an internal link")
        #end debug section

        if os.path.exists(new_file):
            #open the already-created page.
            new_view = window.open_file(new_file)
        else:
            #Create a new file and slap in the default text.
            new_view = window.new_file()
            default_text = "# {0}\n\nWrite about {0} here.".format(link)
            new_view.run_command('append', {'characters': default_text})
            new_view.set_name("%s.wiki" % link)
            new_view.set_syntax_file("Packages/Wiki/Wiki.tmLanguage")
            