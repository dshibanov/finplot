import sys, os, time
# from tensortrade.env.generic.multy_symbol_env import *

# from tensortrade.env.generic.environment import *
# import tensortrade.env.default as default

from pprint import pprint
import finplot as fplt
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QGraphicsView, QComboBox, QLabel
from pyqtgraph.dockarea import DockArea, Dock
from functools import lru_cache
# from threading import Thread
# import yfinance as yf
import numpy as np
import subprocess
import shlex

BG_LIGHT='light'
BG_DARK='dark'
plot_on_main_colors = []

QUOTES = os.getenv('QUOTES')
def set_gruvbox(bg=BG_LIGHT):
    global plot_on_main_colors
    fplt.legend_border_color = '#777'
    fplt.legend_fill_color   = '#3c3836' if bg == BG_DARK else '#3c3836'
    # legend_text_color   = '#ddd6'
    fplt.legend_text_color   = '#fabd2f'
    # soft_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # hard_colors = ['#000000', '#772211', '#000066', '#555555', '#0022cc', '#ffcc00']
    # colmap_clash = ColorMap([0.0, 0.2, 0.6, 1.0], [[127, 127, 255, 51], [0, 0, 127, 51], [255, 51, 102, 51], [255, 178, 76, 51]])
    # foreground = '#000'
    if bg == BG_DARK:
        fplt.background = '#282828'
        fplt.odd_plot_background = '#3c3836'
        plot_on_main_colors = ['red', 'blue', 'green', 'pink']
    else:
        fplt.background = '#ebdbb2'
        fplt.odd_plot_background = '#ebdbb2'
        plot_on_main_colors = ['red', 'blue', 'green', 'pink']
        # plot_on_main_colors = ['#FF5E5B', '#00CECB', '#454851', '#725E54']

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


def get_last_hash():
    # FIXME: there is some bug in next line
    # return subprocess.run(shlex.split("git rev-parse --short HEAD"), check=True, stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    return 'empty'



def get_color(i):
    if i > len(plot_on_main_colors)-1:
        i = i % len(plot_on_main_colors)
    return plot_on_main_colors[i]

def plot(metrics):

    set_gruvbox()
    track = metrics['track']
    trades = metrics['trades']
    plot_params = metrics.get('plot_params', {})
    save_track = plot_params.get('save_track', False)
    suffix = plot_params.get('suffix', '_')
    bg = plot_params.get('bg', 'light')
    title = plot_params.get('title','')
    info = plot_params.get('info', '')

    print(plot_params)


    def get_symbol_name(config, code):
        for s in config['env']['data']['symbols']:
            if s['code'] == code:
                return s['name']

        return 'UNKNOWN_SYMBOL'


    _trades=[]
    track['buy'] = np.nan #pd.NA  # Or use np.nan if NumPy is imported
    track['sell'] = np.nan  #if NumPy is imported

    for t in trades:
        trade = trades[t]
        _trades.append(trade)
        step = trade[0].step

        if trade[0].side.value == 'buy':
            track['buy'].iloc[int(trade[0].step)] = float(trade[0].price)
        else:
            track['sell'].iloc[int(trade[0].step)] = float(trade[0].price)

    track["buy"].iloc[0:len(track)-1] = track["buy"].iloc[1:len(track)]
    track["sell"].iloc[0:len(track)-1] = track["sell"].iloc[1:len(track)]

    # track['sell'] = track['sell'].fillna(-1)
    # track['buy'] = track['buy'].fillna(-1)


    # loop by symbols
    symbol_codes = track['symbol_code'].unique()
    for s in symbol_codes:
        header, ax1, ax2, ax3, ax4, ax5, ax6 = fplt.create_plot(title ='test plot', rows=7)
        header.grid = False
        fplt.add_legend(f"test_name: , date: , hash: {get_last_hash()}, symbol: {get_symbol_name(metrics['config'], s)}", ax=header)
        ax1.grid = False

        current_symbol_track = track[track['symbol_code'] == s]
        current_symbol_track.plot('net_worth', ax=ax2, legend='net_worth', title='some title')
        # track.plot('close', ax=ax1, legend='close', linestyle='solid', width=1.5, color='black', grid=False)
        current_symbol_track.plot('0_price', ax=ax1, legend='close', linestyle='solid', width=1.5, color='black', grid=False)

        for i, c in enumerate(plot_params['plot_on_main'], 0):
            name = c['name']
            color = get_color(i)
            print(name,' ',color)
            current_symbol_track.plot(name, ax=ax1, legend=name, linestyle='solid', width=1.5, color=color, grid=False)

        current_symbol_track.plot('reward', ax=ax3, legend='reward')
        current_symbol_track.plot('action', ax=ax4, legend='action')

        # line styles
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        current_symbol_track.plot('end_of_episode', ax=ax5, legend='end_of_episode', color='#cc241d')
        current_symbol_track.plot('symbol_code', ax=ax6, legend='symbol_code', color='#cc241d')
        # ax1.set_visible(xgrid=True, ygrid=True)
        ax1.set_visible(xgrid=False, ygrid=False)

        # fplt.add_band((30), (35), color='#076678', ax=ax3)
        # fplt.add_rect((100,100), (200,200), color='#cc241d', interactive=False, ax=None)
        # fplt.add_text((150,150), 'texttexttext', color='#076678', anchor=(0,0), ax=ax1)

        # make info string here
        # print lines between open and close
        _open = False
        i = 0
        import math
        trades=[]
        last_order_side = ''

        for index, row in current_symbol_track.iterrows():
            if math.isnan(row["buy"]) == False and math.isnan(row["sell"]) == False:
                print("ERROR: simultanious bus/sell .. at #", index)

            if math.isnan(row["buy"]) == False :
                trades.append({"time":index, "price":row["buy"]})
                last_order_side = 'buy'

            if math.isnan(row["sell"]) == False:
                trades.append({"time":index, "price":row["sell"]})
                last_order_side = 'sell'

        if last_order_side == 'buy':
            current_symbol_track["sell"].iloc[-1] = current_symbol_track["0_price"].iloc[-1]
            trades.append({"time":index, "price":current_symbol_track["0_price"].iloc[-1]})

        fplt.plot(current_symbol_track['buy'], ax=ax1, color='#076678', style='>', legend='buy', width=2)
        fplt.plot(current_symbol_track['sell'], ax=ax1, color='#cc241d', style='<', legend='sell', width=2)
        while i+1 < len(trades):
            fplt.add_line((trades[i]["time"], trades[i]["price"]), (trades[i+1]["time"], trades[i+1]["price"]), color='#e3242b', interactive=False, ax=ax1, style='_')
            i += 2

        fplt.show()


    if save_track:
        track.to_csv(f'test_track_{suffix}.csv', index=False)
    return


    # # ------ 
    # # fplt.axis_height_factor = {0: 2} # top axis is twice as tall as the others
    # # ax1, ax2 = fplt.create_plot(title = title, rows=2)
    # ax1 = fplt.create_plot(title=title)
    # track.plot('net_worth', ax=ax1, legend='net_worth', title='some title')
    # # track.plot('price', ax=ax2, legend='close', linestyle='solid', width=1.5, color='black', grid=False)
    # track.plot('price', ax=ax1, legend='close', linestyle='solid', width=1.5, color='black', grid=False)

    # fplt.show()
    # return


    # # ------
    # _trades=[]
    # for t in trades:
    #     trade = trades[t]
    #     _trades.append(trade)
    #     step = trade[0].step

    #     order_price = float(trade[0].price.real)
    #     if trade[0].side.value == 'buy':
    #         track.loc[(track.index == track.index[trade[0].step]), 'buy'] = order_price #float(trade[0].price.real)
    #         # track.at[trade[0].step, 'buy'] = order_price  # float(trade[0].price.real)
    #     else:
    #         # track.loc[(track.index == trade[0].step), 'sell'] = order_price #float(trade[0].price.real)
    #         track.loc[(track.index == track.index[trade[0].step]), 'sell'] = order_price

    # track["buy"].iloc[0:len(track)-1] = track["buy"].iloc[1:len(track)]
    # track["sell"].iloc[0:len(track)-1] = track["sell"].iloc[1:len(track)]

    # set_gruvbox(bg=bg)

    # if info != '':
    #     header, ax1, ax2, ax3, ax4, ax5, ax6 = fplt.create_plot(title ='test plot', rows=7)
    #     header.grid = False
    #     fplt.add_legend(f"{info}", ax=header)
    # else:
    #     # ax1, ax2, ax3, ax4, ax5, ax6 = fplt.create_plot(title ='test plot', rows=6)
    #     ax1, ax2 = fplt.create_plot(title = title, rows=2)

    # ax1.grid = False

    # fplt.axis_height_factor = {0: 2} # top axis is twice as tall as the others

    # track.plot('net_worth', ax=ax1, legend='net_worth', title='some title')
    # # track.plot('close', ax=ax1, legend='Price close', linestyle='solid', width=1.5, color='black', grid=False)
    # track.plot('price', ax=ax2, legend='close', linestyle='solid', width=1.5, color='black', grid=False)
    # # track.plot('reward', ax=ax3, legend='reward')
    # # track.plot('action', ax=ax4, legend='action')

    # fplt.show()
    # return
    #     # Adding SMA lines
    # # if 'sma_fast' in track.columns and 'sma_slow' in track.columns:
    # #     track.plot('sma_fast', ax=ax1, legend='Fast SMA', color='green', width=1.5)
    # #     track.plot('sma_slow', ax=ax1, legend='Slow SMA', color='red', width=1.5)

    # # # line styles
    # # # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    # # track.plot('end_of_episode', ax=ax5, legend='end_of_episode', color='#cc241d')
    # # track.plot('symbol_code', ax=ax6, legend='symbol_code', color='#cc241d')
    # # ax1.set_visible(xgrid=True, ygrid=True)
    # ax1.set_visible(xgrid=False, ygrid=False)

    # # fplt.add_band((30), (35), color='#076678', ax=ax3)
    # # fplt.add_rect((100,100), (200,200), color='#cc241d', interactive=False, ax=None)
    # # fplt.add_text((150,150), 'texttexttext', color='#076678', anchor=(0,0), ax=ax1)

    # # make info string here
    # # print lines between open and close
    # _open = False
    # i = 0
    # import math
    # trades=[]
    # last_order_side = ''
    # # for index, row in df.iterrows():

    # # print(" 2 ")
    # # pprint(track)
    # for index, row in track.iterrows():
    #     if math.isnan(row["buy"]) == False and math.isnan(row["sell"]) == False:
    #         print("ERROR: simultanious bus/sell .. at #", index)

    #     if math.isnan(row["buy"]) == False :
    #         trades.append({"time":index, "price":row["buy"]})
    #         last_order_side = 'buy'

    #     if math.isnan(row["sell"]) == False:
    #         trades.append({"time":index, "price":row["sell"]})
    #         last_order_side = 'sell'

    # if last_order_side == 'buy':
    #     track["sell"].iloc[-1] = track["close"].iloc[-1]
    #     trades.append({"time":index, "price":track["close"].iloc[-1]})

    # # print(" 3 ")
    # # pprint(track['buy'].head(100))
    # # print(track['buy'].head(100))
    # fplt.plot(track['buy'], ax=ax1, color='#076678', style='>', legend='buy', width=2)
    # fplt.plot(track['sell'], ax=ax1, color='#cc241d', style='<', legend='sell', width=2)
    # while i+1 < len(trades):
    #     # fplt.add_line((trades[i]["time"], trades[i]["price"]), (trades[i+1]["time"], trades[i+1]["price"]), color='#3c3836', interactive=False, ax=ax1, style='_')
    #     fplt.add_line((trades[i]["time"], trades[i]["price"]), (trades[i+1]["time"], trades[i+1]["price"]), color='#e3242b', interactive=False, ax=ax1, style='_')
    #     i += 2

    # fplt.show()

    # if save_track:
    #     track.to_csv(f'test_track_{suffix}.csv', index=False)
