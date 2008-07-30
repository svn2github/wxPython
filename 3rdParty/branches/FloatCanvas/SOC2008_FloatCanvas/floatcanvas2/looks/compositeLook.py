from look import Look

class CompositeLook(Look):
    def __init__( self, looks ):
        self.looks = looks
        
    def Apply(self, renderer):
        for look in self.looks:
            if look:
                look.Apply( renderer )

