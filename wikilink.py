import sublime, sublime_plugin, os, re

class WikiLinkCommand(sublime_plugin.TextCommand):
    
    # Regexes from http://stackoverflow.com/questions/1071191/detect-urls-in-a-string-and-wrap-with-a-href-tag
    pat_url = re.compile(  r'''
                     (?x)( # verbose identify URLs within text
       (http|https|mailto) # make sure we find a resource type
                       :// # ...needs to be followed by colon-slash-slash
            (\w+[:.]?){2,} # at least two domain groups, e.g. (gnosis.)(cx)
                      (/?| # could be just the domain name (maybe w/ slash)
                [^ \n\r"]+ # or stuff then space, newline, tab, quote
                    [\w/]) # resource name ends in alphanumeric or slash
         (?=[\s\.,>)'"\]]) # assert: followed by white or clause ending
                         ) # end of match group
                           ''')
    pat_email = re.compile(r'''
                    (?xm)  # verbose identify URLs in text (and multiline)
                 (?=^.{11} # Mail header matcher
         (?<!Message-ID:|  # rule out Message-ID's as best possible
             In-Reply-To)) # ...and also In-Reply-To
                    (.*?)( # must grab to email to allow prior lookbehind
        ([A-Za-z0-9-]+\.)? # maybe an initial part: DAVID.mertz@gnosis.cx
             [A-Za-z0-9-]+ # definitely some local user: MERTZ@gnosis.cx
                         @ # ...needs an at sign in the middle
              (\w+\.?){2,} # at least two domain groups, e.g. (gnosis.)(cx)
         (?=[\s\.,>)'"\]]) # assert: followed by white or clause ending
                         ) # end of match group
                           ''')

    def run(self, edit):        
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        #find the cursor
        location = self.view.sel()[0]
        
        # find the link text under the cursor
        link = self.view.substr(self.view.extract_scope(location.a))
        
        if "markup.underline.link" not in self.view.scope_name(location.a):
            sublime.status_message("Can only handle links!")
            return

        if (self.pat_url.match(link)):
           sublime.status_message("Trying to open " + link)
           sublime.active_window().run_command('open_url', {"url": link})
           return

        if (self.pat_email.match(link)):
            sublime.status_message("Trying to mail " + link)
            sublime.active_window().run_command('open_url', {"url": "mailto:"+link})

        # TODO: Make a safe filename
        
        #okay, we're good. Keep on keepin' on.        
        
        #compile the full file name and path.
        # TODO: Select the extension based on scope
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
            # Open the already-created page.
            new_view = window.open_file(new_file)
        else:
            # Create a new file and slap in the default text.
            new_view = window.new_file()
            # TODO: Select header character based on scope
            default_text = "= {0}\n\nWrite about {0} here.".format(link)
            new_view.run_command('append', {'characters': default_text})
            new_view.set_name("%s.wiki" % link)
            new_view.set_syntax_file(self.view.settings().get("syntax"))