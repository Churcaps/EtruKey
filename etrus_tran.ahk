#NoTrayIcon

k_pressed := false
p_pressed := false
t_pressed := false
s_pressed := false
plus_pressed := false
h_pressed := false

$k::
{
    global k_pressed
    k_pressed := true
    SetTimer ResetK, -1000
}

$p::
{
    global p_pressed
    p_pressed := true
    SetTimer ResetP, -1000
}

$t::
{
    global t_pressed
    t_pressed := true
    SetTimer ResetT, -1000
}

$s::
{
    global s_pressed
    s_pressed := true
    SetTimer ResetS, -1000
}

$+::
{
    global s_pressed
    global plus_pressed

    if s_pressed
    {
        if plus_pressed
        {
            GetKeyState("Capslock", "T") ? SendText("Ŝ") : SendText("ŝ")
            plus_pressed := false
            return
        }

        plus_pressed := true
        SetTimer ResetPlus, -200
    }
}

$h::
{
    global k_pressed
    global p_pressed
    global t_pressed
    global s_pressed
    global h_pressed

    if k_pressed
    {
        SendText("χ")
        k_pressed := false
    }
    else if p_pressed
    {
        SendText("ϕ")
        p_pressed := false
    }
    else if t_pressed
    {
        SendText("θ")
        t_pressed := false
    }
    else if s_pressed
    {
        if h_pressed
        {
            SendText("Ꮥ")
            h_pressed := false
            return
        }

        h_pressed := true
        SetTimer ResetH, -200
    }
}

ResetK()
{
    global k_pressed
    k_pressed := false
}

ResetP()
{
    global p_pressed
    p_pressed := false
}

ResetT()
{
    global t_pressed
    t_pressed := false
}

ResetS()
{
    global s_pressed
    s_pressed := false
}

ResetPlus()
{
    global plus_pressed

    if plus_pressed
    {
        GetKeyState("Capslock", "T") ? SendText("Ṡ") : SendText("ṡ")
        plus_pressed := false
    }
}

ResetH()
{
    global h_pressed
    global s_pressed

    if h_pressed
    {
        SendText("Ꭶ")
        h_pressed := false
    }

    s_pressed := false
}