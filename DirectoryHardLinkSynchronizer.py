import os

# We use the Pathlib standard package, which is available in Python 3.4 and higher
import pathlib

# Please ensure the the Watchdog package is installed
import watchdog.observers
import watchdog.events


class DirectoryHardLinkSynchronizer(watchdog.events.FileSystemEventHandler):
    """Synchronize a target directory to a source directory continuously using hard-links.
    The source directory may not have subdirectories"""
    def __init__(self, srcDir, dstDir):
        self.initialCopyMade = False
        self.skipGlobs = []        # An iterable containing glob expressions
        self.srcDir = pathlib.Path(srcDir).resolve()
        if not self.srcDir.is_dir():
            raise NotADirectoryError("Source directory {} does not exist".format(srcDir))
        self.dstDir = pathlib.Path(dstDir)
        
    def Start(self):
        self.PerformInitialCopy()
        observer = watchdog.observers.Observer()
        observer.schedule(self, str(self.srcDir), recursive = False)
        observer.start()
        return observer;
        

    def _shouldSkip(self, filePath):
        return any( (pathlib.Path(filePath).match(pattern) for pattern in self.skipGlobs) )

    def _tryLink(self, src, dst):
        try:
            os.link(str(src), str(dst))
        except FileExistsError:
            # FIXME: Verify same inode number
            pass

    def PerformInitialCopy(self):
        self.dstDir.mkdir(exist_ok = True)
        self.dstDir = self.dstDir.resolve()
        for entry in self.srcDir.iterdir():
            assert(not entry.is_dir())
            if not self._shouldSkip(entry):
                src = str(entry)
                dst = str(self.dstDir / entry.name)
                self._tryLink(src, dst)

    def _translatePathToTargetDir(self, src):
        rp = pathlib.Path(src).relative_to(self.srcDir)
        dp = self.dstDir / rp
        return dp
        
    def _finishSyncIfNecessary(self):
        "Perform an initial sync if necessary. Return False if it was performed, True otherwise"
        if not self.initialCopyMade:
            self.PerformInitialCopy()
            self.initialCopyMade = True
            return False
        
        return True
    
    def on_created(self, event):
        assert(not event.is_directory)
        if self._finishSyncIfNecessary():
            self._tryLink(event.src_path, self._translatePathToTargetDir(event.src_path))

        super().on_created(event)
    
    def _delFile(self, src_path):
        try:
            self._translatePathToTargetDir(src_path).unlink()
        except FileNotFoundError:
            pass
        
    def on_deleted(self, event):
        assert(not event.is_directory)
        self._finishSyncIfNecessary()
        self._delFile(event.src_path)
        super().on_deleted(event)
        
    # FIXME: Add on_moved
    #def on_moved(self, event):
        
    #    super().on_moved(self, event)