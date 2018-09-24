



def device_type(request):
    if request.user_agent.is_pc:
        return 'pc'
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return 'mobile'