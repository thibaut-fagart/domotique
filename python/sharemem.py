#! /usr/bin/env python
import os, sys, types, struct, time

class Error(Exception): pass

###########################################################
#
# Shmarea
#
###########################################################

import ipcmem

class Symbarea:
    def __init__( self, name, addr, type, offset ):
        self.name = name
        self.addr = addr 
        self.type = type
        self.size = struct.calcsize( type )
        self.offset = offset

class Shmarea:
    """ zone de command/status a l'interieur d'une partition  """

    def __init__(self, id, offset, size):
        """ constructeur. """
        self._id          = id   
        self._size        = size
        if type( self._id ) != types.IntType: 
            raise Error, 'the type of id parameter should be a integer'
        shmid = ipcmem.getid( self._id, size, ipcmem.IPC_CREAT | 0666 )
        self._shmaddr = ipcmem.attach( shmid, 0, 0 )
        self._name='key=0x%x' % self._id
        self._area_offset = offset
        self._symbols     = {}

    def _read( self, offset, size ):
        return ipcmem.read( offset, size )
        
    def _write( self, offset, data ):
        return ipcmem.write( offset, data )

    def define_word(self, name, offset, type='i'):
        """ definit le nom et l'adresse d'un mot dans la zone """
        self._symbols[name] = Symbarea( name, self._shmaddr + self._area_offset + offset, type, offset )

    def dump(self):
        offset_names = [ (s.offset, s.name) for s in self._symbols.values() ]
        offset_names.sort()
        for o, name in offset_names:
            symb  = self._symbols[name]
            value = struct.unpack( symb.type, self._read( symb.addr, symb.size ) )[0]
            print 'Shmarea(%s)+%08x: %8s %s' % (self._name, symb.offset, `value`, symb.name)
    
    def __getattr__(self, name):
        """ lit la valeur d'un mot en memoire """
        symb  = self._symbols[name]
        return struct.unpack( symb.type, self._read( symb.addr, symb.size ) )[0]
        
    def __setattr__(self, name, value):
        if name[0] == '_':
            self.__dict__[name] = value
        else:
            """ ecrit un mot en memoire """
            symb  = self._symbols[name]
            self._write( symb.addr, struct.pack(symb.type,value))
    def has_word( self, name ):
        return name in self._symbols

###########################################################
#
# Globshm
#
###########################################################

class Homeshm( object ):
    _instance = None
    defwords = [
        ( 'connectState'       , 'i'),
        ( 'lastPacketCuisine'  , 'i'),
        ( 'lastPacketSdb'      , 'i'),
        ( 'lastPacketChambre'  , 'i'),
        ( 'delayNoSound'       , 'i'),
        ( 'tempExt'            , 'f'),
        ( 'humExt'             , 'f'),
        ( 'tempPC'             , 'f'),
        ( 'humPC'              , 'f'),
        ( 'tempCave'           , 'f'),
        ( 'humCave'            , 'f'),
        ( 'tempSdb'            , 'f'),
        ( 'humSdb'             , 'f'),
        ( 'tempSalon'          , 'f'),
        ( 'humSalon'           , 'f'),
        ( 'bascule'            , 'i'),
        ( 'audioSdbPower'      , 'i'),
        ( 'audioSalonPower'    , 'i'),
        ( 'audioCuisinePower'  , 'i'),
        ( 'audioChambrePower'  , 'i'),
        ( 'VMCMan'             , 'i'),
        ( 'VMCPower'           , 'i'),
        ( 'ventiloSdbPower'    , 'i'),
        ( 'ventiloSdbReq'      , 'i'),
        ( 'ventiloSdbSpeed'    , 'i'),
        ( 'rpmSdb'             , 'i'),
        ( 'ventiloCouloirPower', 'i'),
        ( 'ventiloCouloirReq'  , 'i'),
        ( 'ventiloCouloirSpeed', 'i'),
        ( 'rpmCouloir'         , 'i'),
        ( 'forceChaudiere'     , 'i'),
        ( 'presenceCave'       , 'i'),
        ( 'porteFermee'        , 'i'),
        ( 'audioMan'           , 'i'),
        ( 'audioMaxDelay'      , 'i'),
        ( 'audioCurrentDelay'  , 'i'),
        ( 'basculTemp'         , 'i'),
        ( 'timeValOld'         , 'i'),
        ( 'tempExtEte'         , 'i'),
    ]
    words = [ w for w, t in defwords]

    def __new__( cls ):
        if cls._instance is None:
            cls._instance = object.__new__( cls )
        return cls._instance
    def __init__( self, ipcusrkey ):
        key = ipcmem.ftok( '/usr', ipcusrkey )
        try:
            self._shm = Shmarea( key   , 0, 0x1024 )
        except:
            raise Error, 'cannot open ipcshm(key=0x%x)' % ipcusrkey
        
        offset = 0
        for word, wtype in Globshm.defwords:
            self._shm.define_word( word, offset=offset, type=wtype)
            offset +=  struct.calcsize( wtype )
    def __getattr__( self, attr ):
        if attr in Globshm.words:
            return getattr( self._shm, attr )
        else:
            raise AttributeError, 'object(Homeshm) has no attribute "%s"' % attr
    def __setattr__( self, attr, value ):
        if attr[0] == '_':
            self.__dict__[attr] = value
        else:
            setattr( self._shm, attr, value )
    def dump( self ):
        self._shm.dump()
    def reset( self ):
        for word in Globshm.words:
            setattr( self._shm, word, 0 )

class Globshm( Homeshm ):
    def __init__( self ):
        Homeshm.__init__( self, 0x16 )

if __name__=='__main__':
    simshm  = Globshm()
    

