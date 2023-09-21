# all analitical plot functionality is here

# from tensortrade.env.generic.multy_symbol_env import *
from pprint import pprint
import sys, os, time
sys.path.append(os.getcwd())
import finplot as fplt
import pandas as pd

BG_LIGHT='light'
BG_DARK='dark'

def set_gruvbox(bg=BG_LIGHT):
    fplt.legend_border_color = '#777'
    fplt.legend_fill_color   = '#3c3836' if bg == BG_DARK else '#3c3836'
    # legend_text_color   = '#ddd6'
    fplt.legend_text_color   = '#fabd2f'
    # soft_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # hard_colors = ['#000000', '#772211', '#000066', '#555555', '#0022cc', '#ffcc00']
    # colmap_clash = ColorMap([0.0, 0.2, 0.6, 1.0], [[127, 127, 255, 51], [0, 0, 127, 51], [255, 51, 102, 51], [255, 178, 76, 51]])
    # foreground = '#000'
    fplt.background = '#282828' if bg == BG_DARK else '#ebdbb2'
    # fplt.odd_plot_background = '#504945'if bg == BG_DARK else '#669'
    fplt.odd_plot_background = '#3c3836'if bg == BG_DARK else '#ebdbb2'

    # candle_bull_color = '#26a69a'
    # candle_bear_color = '#ef5350'
    # candle_bull_body_color = background
    # volume_bull_color = '#92d2cc'
    # volume_bear_color = '#f7a9a7'
    # volume_bull_body_color = volume_bull_color
    # volume_neutral_color = '#bbb'
    # poc_color = '#006'
    # band_color = '#d2dfe6'
    # cross_hair_color = '#0007'
    # draw_line_color = '#000'
    # draw_done_color = '#555'


def plot_history(history):
    series = history["series"]
    trades = history["trades"]

    # set_gruvbox(bg='dark')
    set_gruvbox()

    # x = series[0]
    # plot it here with finplot
    # add other series also
    # for s in series:
        # plot(s)
        # .. etc
    pprint(series)
    # series.plot('net_worth')
    # ax1, ax2 = fplt.create_plot('BitMEX %s heikin-ashi price history' % symbol, rows=2)
    ax1, ax2, ax3, ax4 = fplt.create_plot('test plot', rows=4)

    series.plot('net_worth', ax=ax1, legend='net_worth')
    # series.plot('close', ax=ax1, legend='close', linestyle='solid', linewidth=5.1, color='black')
    series.plot('close', ax=ax1, legend='close', linestyle='solid', width=2.1, color='black')
    # for line in ax1.get_lines():
    #     if line.get_label() == 'close':
    #         line.set_linewidth(5)

    series.plot('reward', ax=ax2, legend='reward')
    series.plot('action', ax=ax3, legend='action')

    # line styles
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    series.plot('end_of_episode', ax=ax4, legend='end_of_episode', color='#cc241d')
    # bbwp.squeeze().plot(ax=ax)
    ax1.set_visible(xgrid=True, ygrid=True)
    fplt.show()
    # add trades

# def make_symbols(num_symbols=5, length=666):
#     symbols=[]
#     for i in range(num_symbols):
#         spread = 0.01
#         commission=0
#         if i == 2:
#             commission=0
#             spread=1.13
#         elif i == 4:
#             commission=0
#             spread=3.66
#         symbols.append(make_sin_symbol("AST"+str(i), i, commission=commission, spread=spread, length=length))
#     return symbols

def test_plot_history():

    track = pd.read_csv('tests/test_track.csv')
    # pprint(track)
    # symbols = make_symbols()
    # config = {"symbols": symbols,
    #           "reward_window_size": 7,
    #           "window_size": 1,
    #           "max_allowed_loss":100,
    #           "multy_symbol_env": True
    #          }

    # dataset = pd.concat([config["symbols"][i]["feed"] for i in range(len(config["symbols"]))])
    # history = {"series":dataset,
    history = {"series":track,
               "trades":[]}

    # TODO: do some simulation to get trades
    #   - how to extract trades?? 
    #
    #   надо посмотреть что там будет 


    plot_history(history)



if __name__ == "__main__":
    test_plot_history()
    #import matplotlib.pyplot as plt
    #import numpy as np

    ##define x and y values
    #x = np.linspace(0, 10, 100)
    #y1 = np.sin(x)*np.exp(-x/3)
    #y2 = np.cos(x)*np.exp(-x/5)

    ##create line plot with multiple lines
    #plt.plot(x, y1, linewidth=3)
    #plt.plot(x, y2, linewidth=1)

    ##display plot
    #plt.show()





