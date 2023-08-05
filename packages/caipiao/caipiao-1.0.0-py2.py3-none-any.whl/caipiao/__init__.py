from random import randint, random, sample

def num_p(balls):
    if balls:
        if isinstance(balls,list) or isinstance(balls,tuple):
            last_reslut = ['0{}'.format(int(ball)) if int(ball)<10 else str(int(ball)) for ball in balls] 
        else:
           last_reslut = '0{}'.format(int(balls)) if int(balls)<10 else str(int(balls))
        return last_reslut
    else:
        return ''


def random_ssq(num=1,reds_pre=None,blue_pre=None):
    result = []
    for n in range(num):
        if reds_pre is None:
            reds = [] 
            while len(reds) < 6:
                red_ball = randint(1,33)
                if red_ball not in reds:
                    reds.append(red_ball)
        if blue_pre is None:
            blue = randint(1,16)
        
        reds.sort()
        red_balls = num_p(reds)
        blue_ball = num_p(blue)
        result.append(' '.join(red_balls) + ' + '+ blue_ball)
    return '\n'.join(result)


def random_dlt(num=1,reds_pre=None,blue_pre=None):
    result = []
    for n in range(num):
        if reds_pre is None:
            reds = sample([n for n in range(1,36)],5)
        if blue_pre is None:
            blues = sample([n for n in range(1,13)],2)
        
        reds.sort()
        blues.sort()
        red_balls = num_p(reds)
        blue_balls = num_p(blues)
        result.append(' '.join(red_balls) + ' + '+ ' '.join(blue_balls))
    return '\n'.join(result)
