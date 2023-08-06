import matplotlib.pyplot as _plt
from collections import deque
import inspect as _inspect
from typing import Sequence as _Sequence


class __DirectPlot:
    """Internal class used for the internal singleton object __dp"""

    def __init__(self, titles: _Sequence[str], linesPerSubplot: int = 4, showMarker: bool = True, maxPoints: int = 10000) -> None:
        self._create(titles, linesPerSubplot, showMarker, maxPoints)

    # At this time, it is better not to have a destructor.
    # Reason: The implementation below seems to cause additional exceptions
    #         in case the program is ended due an exception.
    # def __del__(self) -> None:
    #     self.close()

    def _create(self, titles: _Sequence[str], linesPerSubplot: int = 4, showMarker: bool = True, maxPoints: int = 10000) -> None:
        if isinstance(titles, str):
            titles = (titles, )
        
        self.titles = titles
        self.maxPoints = maxPoints
        self.linesPerSubplot = linesPerSubplot

        self.subPlotCount = len(titles)
        if self.subPlotCount<1 or self.subPlotCount>3:
            raise ValueError(f"ERROR in directplot: YOU PROVIDED {self.subPlotCount} PLOT-TITLES. ONLY 1...3 ARE ALLOWED!")

        if not (_plt.isinteractive()): 
            _plt.ion()

        self.xDeques=[]
        self.yDeques=[]
        self.lines2d=[]

        self.fig, self.axs = _plt.subplots(1, self.subPlotCount, figsize=(4*self.subPlotCount, 3.5))
        # Ensure self.axs is an iterable, even in case of just one sub-plot:
        if self.subPlotCount==1: self.axs = (self.axs, )

        for i, title in enumerate(titles):
            self.axs[i].set_title(title)
            self.axs[i].set_xlabel("xlabel")
            self.axs[i].set_ylabel("ylabel")

            for plot_idx in range(linesPerSubplot):
                newXdeque = deque(maxlen=self.maxPoints)
                self.xDeques.append(newXdeque)
                newYdeque = deque(maxlen=self.maxPoints)
                self.yDeques.append(newYdeque)
                line2d, = self.axs[i].plot(newXdeque, newYdeque, label=f"id {i*linesPerSubplot+plot_idx}", marker="." if showMarker else "") # marker='o',
                self.lines2d.append(line2d)

            self.axs[i].legend(loc='upper right')
        
        _plt.tight_layout()
        self._redraw()

    def close(self) -> None:
        try:
            _plt.close(self.fig)
            del(self.xDeques)
            del(self.yDeques)
            del(self.lines2d)
            del(self.fig)
            del(self.axs)
        except AttributeError:
            raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO PLOT-WINDOW AVAILABLE. DID YOU ALREADY CLOSE IT?")

    def waitforclose(self, msg: str = None) -> None:
        self.fig.canvas.set_window_title(msg or " "+5*" ===== DONE - PLEASE CLOSE THIS WINDOW "+"=====")
        self._redraw()
        _plt.ioff()
        _plt.show()
        del(self.xDeques)
        del(self.yDeques)
        del(self.lines2d)
        del(self.fig)
        del(self.axs)

    def clear(self) -> None:
        self.close()
        self._create(self.titles, self.linesPerSubplot)

    def add(self, id: int, x: float, y: float, refresh: bool = True) -> None:
        if id<0 or id>=self.subPlotCount*self.linesPerSubplot:
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")

        self.xDeques[id].append(x)
        self.yDeques[id].append(y)
        self.lines2d[id].set_data(self.xDeques[id], self.yDeques[id])
        if refresh:
            ax_idx = id // self.linesPerSubplot
            self.axs[ax_idx].relim()
            self.axs[ax_idx].autoscale_view()
            self._redraw()

    def refresh(self) -> None:
        try:
            for ax in self.axs:
                ax.relim()
                ax.autoscale_view()
            self._redraw()
        except AttributeError:
            raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO PLOT-WINDOW AVAILABLE. DID YOU ALREADY CLOSE IT?")
    
    def showMarker(self, show: bool = True, id: int = None) -> None:
        if id is None:
            # Alle Linien/Datenserien aktualisieren:
            for line in self.lines2d:
                line.set_marker("." if show else "")
            # Alle Legenden aktualisieren:
            for ax in self.axs:
                ax.legend(loc='upper right')
        else:
            # Nur eine Linie/Datenserie mit Legende aktualisieren:
            if id<0 or id>=len(self.lines2d):
                raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
            self.lines2d[id].set_marker("." if show else "")
            ax_idx = id // self.linesPerSubplot
            self.axs[ax_idx].legend(loc='upper right')
        # Der Einfachheit halber den ganzen Plot aktualisieren:
        self._redraw()

    def label(self, id: int, label: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        self.lines2d[id].set_label(label)
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].legend(loc='upper right')
        self._redraw()

    def title(self, id: int, title: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].set_title(title)
        self.titles[ax_idx] = title
        self._redraw()

    def xylabel(self, id: int, xlabel: str, ylabel: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].set_xlabel(xlabel)
        self.axs[ax_idx].set_ylabel(ylabel)
        self._redraw()

    def _redraw(self) -> None:
        #print('.', end='', flush=True)
        #_plt.pause(0.001)
        # Source: https://matplotlib.org/stable/users/explain/interactive_guide.html#explicitly-spinning-the-event-loop
        self.fig.canvas.draw_idle()    # Python-Docu: Request a widget redraw once control returns to the GUI event loop.
        self.fig.canvas.flush_events() # Python-Docu: This will run the GUI event loop until all UI events currently waiting have been processed.
        # self.fig.canvas.draw()       # Python-Docu: It is important that this method actually walk the artist tree even if not output is produced
        # self.fig.canvas.start_event_loop(0.001)
