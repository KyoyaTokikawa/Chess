from src.game_master import *
import time
gameNo = 0

gamerecord_dic = gamerecord()
# adam or sgd, batchsize, epsilon, reword, Rate of count for reward
sample_a = ['Adam', 1024, 0.5, 0.2, 0.05]
parameter = sample_a
white_agent = Agent(64, len(gamerecord_dic), parameter)
black_agent = Agent(64, len(gamerecord_dic), parameter)

print('test')

AI_count_win = 0
AI_count_lose = 0
draw = 0
white_win = 0
black_win = 0
print(len(gamerecord_dic))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
a = a
while True:
    gameNo += 1
    instance = master(white_agent, black_agent, gamerecord_dic, device)
    much, white, black = instance(gameNo)
    if much == 0:
        draw += 1
        much = -0.1
    elif much == 1:
        white_win += 1
    elif much == -1:
        black_win += 1
    for w_val in white:
        if len(w_val[3]) == 0:
            a = a
        white_agent.memorize(w_val[0], torch.tensor([w_val[1]]), w_val[2], [w_val[3]], torch.LongTensor([w_val[4] * much]))
    if gameNo % 1 == 0:
        start = time.time()
        white_agent.update_q_network()
        end = time.time()
        
    # for b_val in black:
    #     black_agent.memorize(b_val[0], b_val[1], b_val[2], torch.LongTensor([b_val[3] * -1 * much]))
    #     black_agent.update_q_network()

    if gameNo % 1 == 0:
        with open('result.txt', 'a') as f:
            draw_result = 'draw:' + str(draw)
            white_result = 'white:' + str(white_win)
            black_result = 'black:' + str(black_win) 
            print(str(gameNo) + ' ' + draw_result + ' ' + white_result + '(' + str(AI_count_win) + ')' + ' ' + black_result+ '(' + str(AI_count_lose) + ')', file=f)
            print('random' + ':' + str(w_val[5]) + '/' +'AI' + ':' + str(w_val[6]) +'(' + str(math.ceil(w_val[6] / (w_val[5] + w_val[6]) * 100)) +'%)' + ' last:' + w_val[7], file=f)
            print(end - start, file=f)
        if w_val[7] == 'AI' and much == 1:
            AI_count_win += 1
        elif w_val[7] == 'AI' and much == -1:
            AI_count_lose += 1
        print(str(gameNo) + ' ' + draw_result + ' ' + white_result + '(' + str(AI_count_win) + ')' + ' ' + black_result+ '(' + str(AI_count_lose) + ')')
        print('random' + ':' + str(w_val[5]) + '/' +'AI' + ':' + str(w_val[6]) +'(' + str(math.ceil(w_val[6] / (w_val[5] + w_val[6]) * 100)) +'%)' + ' last:' + w_val[7])
        print(end - start)
        print('\n')


