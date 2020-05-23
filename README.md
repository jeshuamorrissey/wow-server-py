# Python Vanilla WoW Server
This repo contains a built-from-scratch World of Warcraft (Vanilla) server. The goal of this server is to be more for small groups of friends to play (e.g. many quests will change the world permanently for everyone), or for a single-player experience. It is still a long, long way away from being finished, but it is also a fun side project.

## Starting the server
To run the server, start by [installing bazel](https://docs.bazel.build/versions/master/install.html). Then:

```
$ git clone https://github.com/jeshuamorrissey/wow-server-py.git
$ bazel run //:wow_server
```

If you are on Windows, you will have to pass `--experimental_enable_runefiles` to Bazel or it won't find the data.
