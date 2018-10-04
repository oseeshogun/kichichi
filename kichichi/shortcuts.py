from dreamteam.models import Dreamteam



def device_type(request):
    if request.user_agent.is_pc:
        return 'pc'
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return 'mobile'

def dreamteamid(user):
    for d in Dreamteam.objects.all():
        if d.member1 == user or d.member2 == user:
            return d.id
    return False

def dreamteampartern(user):
    for d in Dreamteam.objects.all():
        if d.member1 == user or d.member2 == user:
            if d.member1 == user:
                return d.member2
            else:
                return  d.member1
    return False