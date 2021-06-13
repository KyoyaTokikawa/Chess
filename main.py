from src.game_master import *

gameNo = 0

gamerecord_dic = gamerecord()
white_agent = Agent(64, len(gamerecord_dic))
black_agent = Agent(64, len(gamerecord_dic))

draw = 0
white_win = 0
black_win = 0
print(len(gamerecord_dic))
print(torch.cuda.is_available())
a = a
while True:
    gameNo += 1
    instance = master(white_agent, black_agent, gamerecord_dic)
    much, white, black = instance(gameNo)
    if much == 0:
        draw += 1
    elif much == 1:
        white_win += 1
    elif much == -1:
        black_win += 1
    for w_val in white:
        white_agent.memorize(w_val[0], w_val[1], w_val[2], torch.LongTensor([w_val[3] * 1 * much]))
        if gameNo % 15 == 0:
            white_agent.update_q_network()
    # for b_val in black:
    #     black_agent.memorize(b_val[0], b_val[1], b_val[2], torch.LongTensor([b_val[3] * -1 * much]))
    #     black_agent.update_q_network()

    if gameNo % 1 == 0:
        with open('result.txt', 'a') as f:
            draw_result = 'draw:' + str(draw)
            white_result = 'white:' + str(white_win)
            black_result = 'black:' + str(black_win) 
            print(str(gameNo) + ' ' + draw_result + ' ' + white_result + ' ' + black_result, file=f)