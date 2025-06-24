;#NoTrayIcon

k_pressed := false
p_pressed := false
t_pressed := false
s_pressed := false
plus_pressed := false
h_pressed := false

SetKeyDelay(-1)

~k::
{
    global k_pressed
    k_pressed := true
    SetTimer ResetK, -300
}

~p::
{
    global p_pressed
    p_pressed := true
    SetTimer ResetP, -300
}

~t::
{
    global t_pressed
    t_pressed := true
    SetTimer ResetT, -300
}

~s::
{
    global s_pressed
    s_pressed := true
    SetTimer ResetS, -400
}

$+::
{
    global s_pressed
    global plus_pressed

    if s_pressed
    {
        if plus_pressed
        {
            GetKeyState("Capslock", "T") ? SendInput("{BS 1}Ŝ") : SendInput("{BS 1}ŝ")
            plus_pressed := false
            return
        }

        plus_pressed := true
        SetTimer ResetPlus, -200
    }
}

~h::
{
    global k_pressed
    global p_pressed
    global t_pressed
    global s_pressed
    global h_pressed

    if k_pressed
    {
        GetKeyState("Capslock", "T") ? SendInput("{BS 2}Χ") : SendInput("{BS 2}χ")
        k_pressed := false
    }
    else if p_pressed
    {
        GetKeyState("Capslock", "T") ? SendInput("{BS 2}Φ") : SendInput("{BS 2}ϕ")
        p_pressed := false
    }
    else if t_pressed
    {
        GetKeyState("Capslock", "T") ? SendInput("{BS 2}Θ") : SendInput("{BS 2}θ")
        t_pressed := false
    }
    else if s_pressed
    {
        if h_pressed
        {
            GetKeyState("Capslock", "T") ? SendInput("{BS 3}Ꮥ") : SendInput("{BS 3}ꮥ")
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
        GetKeyState("Capslock", "T") ? SendInput("{BS 1}Ṡ") : SendInput("{BS 1}ṡ")
        plus_pressed := false
    }
}

ResetH()
{
    global h_pressed
    global s_pressed

    if h_pressed
    {
        GetKeyState("Capslock", "T") ? SendInput("{BS 2}Ꭶ") : SendInput("{BS 2}ꭶ")
        h_pressed := false
    }

    s_pressed := false
}