class config:
    base_link = "https://api.altv.mp"
    all_server_stats_link = "{}/servers".format(base_link)
    all_servers_link = "{}/servers/list".format(base_link)
    server_link = "{}/server".format(base_link) + "/{}"
    server_average_link = "{}/avg".format(base_link) + "/{}/{}"
    server_max_link = "{}/max".format(base_link) + "/{}/{}"