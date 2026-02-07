class Test:
    '''
    '''
    def __init__(self):
        print('Test from chi1205b translator')


class Info:
    '''
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    '''
    def __init__(self):
        self.tech = ['CV', 'CA', 'LSV', 'OCP', 'CP']
        self.options = ['Quiet time in s (qt)']

        self.E_min = -2.4
        self.E_max = 2.4
        self.sr_min = 0.000001
        self.sr_max = 10
        #self.dE_min = 
        #self.sr_min = 
        #self.dt_min = 
        #self.dt_max = 
        #self.ttot_min = 
        #self.ttot_max = 

    def limits(self, val, low, high, label, units):
        if val < low or val > high:
            raise Exception(label + ' should be between ' + str(low) + ' ' +\
                            units  + ' and ' + str(high) + ' ' + units +\
                            '. Received ' + str(val) + ' ' + units)

    def specifications(self):
        print('Model: CH Instruments 1205B (chi1205b)')
        print('Techiques available:', self.tech)
        print('Options available:', self.options)



class CV:
    '''
        **kwargs:
            qt # s, quite time
    '''
    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, 
                 folder, fileName, header, path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = '' 

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        self.validate(Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens)

        # correcting parameters:
        Ei = Eini
        if Ev1 > Ev2:
            eh = Ev1
            el = Ev2
            pn = 'p'
        else:
            eh = Ev2
            el = Ev1
            pn = 'n'
        #nSweeps = nSweeps + 1 # final e from chi is enabled by default

        # building macro:
        self.head = 'c\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=cv\nei=' + str(Ei) + '\neh=' + str(eh) + '\nel=' + \
                    str(el) + '\npn=' + pn + '\ncl=' + str(nSweeps) + \
                    '\nefon\nef=' + str(Efin) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nv=' + str(sr) + '\nsens=' + str(sens)
        self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens):
        info = Info()
        info.limits(Eini, info.E_min, info.E_max, 'Eini', 'V')
        info.limits(Ev1, info.E_min, info.E_max, 'Ev1', 'V')
        info.limits(Ev2, info.E_min, info.E_max, 'Ev2', 'V')
        info.limits(Efin, info.E_min, info.E_max, 'Efin', 'V')
        info.limits(sr, info.sr_min, info.sr_max, 'sr', 'V/s')
        #info.limits(dE, info.dE_min, info.dE_max, 'dE', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')


class LSV:
    '''
        **kwargs:
            qt # s, quiet time
    '''
    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header,
                 path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        self.validate(Eini, Efin, sr, dE, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens) 
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Efin, sr, dE, sens):
        info = Info()
        info.limits(Eini, info.E_min, info.E_max, 'Eini', 'V')
        info.limits(Efin, info.E_min, info.E_max, 'Efin', 'V')
        info.limits(sr, info.sr_min, info.sr_max, 'sr', 'V/s')
        #info.limits(dE, info.dE_min, info.dE_max, 'dE', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')



class CA:
    '''
        **kwargs:
            qt # s, quite time
    '''
    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, 
                 path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens) 
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

        self.validate(Estep, dt, ttot, sens)


    def validate(self, Estep, dt, ttot, sens):
        info = Info()
        info.limits(Estep, info.E_min, info.E_max, 'Estep', 'V')
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')



class OCP:
    '''
        Assumes OCP is between +- 5 V
        **kwargs:
            qt # s, quite time
    '''
    def __init__(self, ttot, dt, folder, fileName, header, path_lib, **kwargs):
        self.ttot = ttot
        self.dt = dt

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        self.validate(ttot, dt)

        self.fileName = fileName
        self.folder = folder
        self.text = ''
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=5' + \
                    '\nel=-5' + '\nsi=' + str(dt) + '\nqt=' + str(qt) +\
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

    def validate(self, ttot, dt):
        info = Info()
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')
        print('All the parameters are valid')


class CP:
    '''
        Chronopotentiometry (CP) translator (GUI-friendly)

        GUI naming (your lab):
            ic      Cathodic Current (A)
            ia      Anodic Current (A)
            he      High E Limit (V)
            het     High E Hold Time (s)
            le      Low E Limit (V)
            let     Low E Hold Time (s)
            ct      Cathodic Time (s)
            at      Anodic Time (s)
            ds      Data Storage Interval (s)
            segment Number of Segments
            ip      Initial Polarity: 'p' (positive/anodic first) or 'n' (negative/cathodic first)

        **kwargs (optional):
            sp      switching priority: 'p' (potential) or 't' (time)
            qt      quiet time (s)
    '''

    def __init__(self,
                 ic, ia,
                 he, het,
                 le, let,
                 ct, at,
                 ds, segment,
                 sens,
                 folder, fileName, header, path_lib,
                 ip='p', **kwargs):

        self.fileName = fileName
        self.folder = folder
        self.text = ''

        # Optional controls
        sp = kwargs.get('sp', 'p')
        qt = kwargs.get('qt', 2)

        # Map GUI naming -> CHI macro naming
        eh  = he
        el  = le
        ehh = het
        elh = let
        tc  = ct
        ta  = at
        si  = ds
        cl  = segment

        # Map initial polarity: GUI uses 'p'/'n', translator/macro uses 'a'/'c'
        # 'p' (positive/anodic first)  -> 'a'
        # 'n' (negative/cathodic first)-> 'c'
        if ip in ('p', 'P'):
            ip_macro = 'a'
        elif ip in ('n', 'N'):
            ip_macro = 'c'
        elif ip in ('a', 'A', 'c', 'C'):
            # allow old style input too
            ip_macro = ip.lower()
        else:
            raise ValueError("ip must be 'p'/'n' (or 'a'/'c'). Received: " + str(ip))

        self.validate(ic, ia, eh, el, tc, ta, cl, si, sens)

        # --- build macro (same style as CV/LSV/CA/OCP) ---
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'

        self.body = 'tech=cp\nic=' + str(ic) + '\nia=' + str(ia) + \
                    '\neh=' + str(eh) + '\nel=' + str(el) + \
                    '\nehh=' + str(ehh) + '\nelh=' + str(elh) + \
                    '\ntc=' + str(tc) + '\nta=' + str(ta) + \
                    '\nip=' + str(ip_macro) + '\nsi=' + str(si) + \
                    '\ncl=' + str(cl) + '\nsp=' + str(sp) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens)

        self.body2 = self.body + '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName
        self.foot  = '\n forcequit: yesiamsure\n'
        self.text  = self.head + self.body2 + self.foot

    def validate(self, ic, ia, eh, el, tc, ta, cl, si, sens):
        info = Info()
        info.limits(eh, info.E_min, info.E_max, 'he/eh', 'V')
        info.limits(el, info.E_min, info.E_max, 'le/el', 'V')
        print('All the parameters are valid')
