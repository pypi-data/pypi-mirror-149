##################################################################
#                                                                #
#.#####...#####...##..##..##..##...####...##......######...####..#
#.##..##..##..##...####...###.##..##......##......##......##.....#
#.#####...#####.....##....##.###..##.###..##......####.....####..#
#.##......##..##....##....##..##..##..##..##......##..........##.#
#.##......##..##....##....##..##...####...######..######...####..#
#................................................................#
#                                                                #
# PlanetaRY spanGLES                                             #
# The bright-side of the light-curve of (ringed) exoplanets      #
#                                                                #
##################################################################
# Jorge I. Zuluaga, Mario Sucerquia, Jaime A. Alvarado (C) 2022  #
##################################################################
#!/usr/bin/env python
# coding: utf-8

# # Pryngles module

# ## Module base
# 
# Goals of the module:
# - Future `base`
# - Basic Classes and functions of the Class.
# - It is based on existing infrastructure.

##HEADER
from pryngles import *
import unittest
#import rebound as rb
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

#Astronomical constants
import rebound as rb
from rebound.units import times_SI,lengths_SI,masses_SI

class Test(unittest.TestCase):
    from pryngles import _base

class Object(PrynglesCommon):
    """
    Global class of object
    """
    def _updateChilds(self,child=None):
        if 'childs' not in self.__dict__:
            self.childs=[]
        if child is not None:
            self.childs+=[child]
    def _updateParent(self,parent=None):
        if 'parent' not in self.__dict__:
            self.parent=parent
        elif parent is not None:
            self.parent=parent

def test_Object(self):
    obj=Object()
    obj._updateParent("parent")
    obj._updateChilds("child1")
    obj._updateChilds("child2")
    self.assertEqual([obj.parent],["parent"],True)
    self.assertEqual(obj.childs,["child1","child2"],True)
Test.test_Object=test_Object
#unittest.main(argv=['first-arg-is-ignored'],exit=False)

def addStar(self,
                 hash=None,
                 center=None,
                 m=1,R=Const.Rsun/Const.au,
                 Prot=0.1,
                 N=1000,
             star=None
            ):
    """
    TO DEVELOPERS:
        This method is for the System class.  It is placed here because when a new parameter
        is added to the initializer of the addObject (being Object Star, Planet, etc.) class
        then the parameters of this ruotine should also change.
    """
    if star is not None:
        self._addObject("star","Star",star)
    else:
        self.stars+=[Star(hash,center,m,R,Prot,N)]
    self._updateSystem()
    return self.stars[-1]

class Star(Object):
    """
    Creates a star.
    """
    def __init__(self,
                 hash=None,
                 center=None,
                 m=1,R=Const.Rsun/Const.au,
                 Prot=0.1,
                 N=1000,
                ):
        #List of arguments: hash,center,m,r,Prot,N
        #Hash of the object
        self.hash=hash
        self.type="Star"

        #Center of the system (object)
        self.center=center
        if self.center is not None:
            self.center._updateChilds(self)
            self._updateParent(self.center)
        
        #Basic common properties
        self.m=m #mass [cu]
        self.R=R #radius [cu]

        #Dynamic parameters
        self.Prot=Prot

        #Sampling parameters
        self.N=N #number of spangles
        
        #Update properties
        self.updateObject(**self.__dict__)

    def updateObject(self,**props):
        self.__dict__.update(props)
        self._updateChilds()
        self._updateParent()

def addPlanet(self,
                 hash=None,
                 center=None,
                 m=masses_SI["msaturn"]/masses_SI["msun"],R=Const.Rsat/Const.au,
                 a=0.2,e=0.6,
                 Prot=0.01,
                 N=1000,
             planet=None
            ):
    if planet is not None:
        self._addObject("planet","Planet",planet)
    else:
        self.planets+=[Planet(hash,center,m,R,a,e,Prot,N)]
    self._updateSystem()
    return self.planets[-1]

class Planet(Object):
    """
    Creates a star.
    """
    def __init__(self,
                 hash=None,
                 center=None,
                 m=masses_SI["msaturn"]/masses_SI["msun"],R=Const.Rsat/Const.au,
                 a=0.2,e=0.6,
                 Prot=0.01,
                 N=1000,
                ):
        #List of arguments: hash,center,m,R,a,e,Prot,N
        #Hash of the object
        self.hash=hash
        self.type="Planet"

        #Center of the system (object)
        if center is None:
            raise ValueError(f"You must provide a valid object for the center.  {center} provided")
        self.center=center
        self.center._updateChilds(self)
        self._updateParent(self.center)
        
        #Basic common properties
        self.m=m #mass [cu]
        self.R=R #radius [cu]

        #Dynamic parameters
        self.Prot=Prot
        
        #Orbital properties
        self.a=a
        self.e=e

        #Sampling parameters
        self.N=N #number of spangles
        
        #Update properties
        self.updateObject(**self.__dict__)
        
    def updateObject(self,**props):
        self.__dict__.update(props)
        self._updateChilds()
        self._updateParent()

def addRing(self,
                 hash=None,
                 center=None,
                 fi=1.5,fe=2.5,
                 i=30*deg,
                 N=1000,
             ring=None
            ):
    if ring is not None:
        self._addObject("ring","Ring",ring)
    else:
        self.rings+=[Ring(hash,center,fi,fe,i,N)]
    self._updateSystem()
    return self.rings[-1]
    
class Ring(Object):
    """
    Creates a star.
    """
    def __init__(self,
                 hash=None,
                 center=None,
                 fi=1.5,fe=2.5,
                 i=0,
                 N=1000,
                ):
        #List of arguments: hash,center,fi,fe,i,N
        #Hash of the object
        self.hash=hash
        self.type="Ring"

        #Center of the system (object)
        if center is None:
            raise ValueError(f"You must provide a valid object for the center.  {center} provided")
        self.center=center
        self.center._updateChilds(self)
        self._updateParent(self.center)

        #Basic common properties
        self.fi=fi
        self.fe=fe
        
        #Orientation
        self.i=i

        #Sampling parameters
        self.N=N #number of spangles
        
        #Update properties
        self.updateObject(**self.__dict__)
        
    def updateObject(self,**props):
        self.__dict__.update(props)
        self._updateChilds()
        self._updateParent()
        
        #Derivative properties
        self.ri=self.fi*self.center.R
        self.re=self.fe*self.center.R

def addObserver(self,
                 center=None,
                 beta=90*deg,lamb=90*deg,
             observer=None
            ):
    if observer is not None:
        self._addObject("observer","Observer",observer)
    else:
        self.observers+=[Observer(center,beta,lamb)]
    self._updateSystem()
    return self.observers[-1]
    
class Observer(Object):
    """
    Creates a star.
    """
    def __init__(self,
                 center=None,
                 beta=90*deg,lamb=90*deg,
                ):
        #List of arguments: center,beta,lamb
        #Hash of the object
        self.hash=hash
        self.type="Observer"

        #Center of the system (object)
        self.center=center
        if self.center is not None:
            self.center._updateChilds(self)
            self._updateParent(self.center)

        #Basic common properties
        self.beta=beta
        self.lamb=lamb

        #Update properties
        self.updateObject(**self.__dict__)
        
    def updateObject(self,**props):
        self.__dict__.update(props)
        self._updateChilds()
        self._updateParent()

System_doc="""
Creates a planetary system.

Examples:

    sys=System()
    sys=System(units=['msun','km','s'])
    sys=System(stars=dict(M=1,R=1))

Initialization (primary) attributes:

    units = ['msun','au','yr']: 
        Units used in calculations following the conventions and signs of rebound. List [3].
        
    stars = None: 
        Stars in the system.
    planets = None: 
        Planets in the system.
    rings = None: 
        Rings in the system.
    observers = None: 
        Observers in the system.
           
        NOTE: Objects are provided either by description or as an object. Those attributes can be lists or 
              a single value.
    
    rebound = True:
        Set True if you want to simulte the orbit of objects (for instance if you want to calculate
        TTVs).  If False it will calculate orbits using Keplerian dynamics.

Other Public (secondary) attributes:

    N: Number of objects in the system.
    No: Numeber of observers

Important private attributes:

    _sim: Rebound simulation object.
""";

import rebound as rb
class System(PrynglesCommon):
    
    def __init__(self,
                 units=['au','yr','msun'],
                 stars=None,planets=None,rings=None,observers=None,
                 rebound=True
                ):
        
        #Initialize rebound
        self.units=units
        self._sim=rb.Simulation()
        self._sim.units=self.units
        self._ul,self._ut,self._um=self.units
        self.G=self._sim.G
        self.ul=rb.units.convert_length(1,self._ul,"m")
        self.um=rb.units.convert_mass(1,self._um,"kg")
        self.GSI=rb.units.convert_G(["m","s","kg"])
        self.ut=np.sqrt(self.ul**3/(self.um*self.GSI))

        #Add components
        self._list2Objects("stars","Star",stars)
        self._list2Objects("planets","Planet",planets)
        self._list2Objects("rings","Ring",rings)
        self._list2Objects("observers","Observer",observers)

        #Behavior
        self.rebound=True
        
        #Update system
        self._updateSystem()
        
    """
    #Freezer
    def addStar(self,star=None):
        self._addObject("star","Star",planet)
        self._updateSystem()
    
    def addPlanet(self,planet=None):
        self._addObject("planet","Planet",planet)
        self._updateSystem()
    
    def addRing(self,ring=None):
        self._addObject("ring","Ring",ring)
        self._updateSystem()
    """
    def _addObject(self,kind,objclass,obj):
        error=""
        try:
            obj.__dict__
            exec(f"self.{kind}s=self.{kind}s+[obj] if len(self.{kind}s)!=0 is not None else [obj]")
            cond=eval(f"obj.type!='{objclass}'")
            if cond:
                error=f"You cannot add a {objclass} with a {obj.type} object"
        except:
            exec(f"self.{kind}s+=self.{kind}s+[obj] if len(self.{kind}s)!=0 else [obj]")
        if error!="":
            exec(f"self.{kind}s.pop()")
            raise AssertionError(error)
        self._updateSystem()
    
    def _updateSystem(self):
        #Count components
        self.Nstars=self.Nplanets=self.Nrings=0
        for obj in "stars","planets","rings":
            exec(f"self.N{obj}=len(self.{obj})")
        self.N=self.Nstars+self.Nplanets+self.Nrings
        self.No=len(self.observers)
        
    def ensambleSystem(self):
        #Ensamble system
        #--CONSISTENCY--
        if self.Nstars==1 and self.Nplanets==1 and self.Nrings==1:
            #Create ringed planet
            self.G=self._sim.G
            
            self._ringedplanet=dict(
                #Behavior
                behavior=dict(shadows=True),
                #Units
                CU=CanonicalUnits(UL=self.ul,UM=self.um),
                #Basic
                Rstar=self.stars[0].R,Rplanet=self.planets[0].R,
                Rint=self.rings[0].fi,Rext=self.rings[0].fe,i=self.rings[0].i,
                a=self.planets[0].a,e=self.planets[0].e,
                #Orbit 
                Mstar=1,x=0,lambq=0,t0=0,kepler=False,
                #Observer
                eobs_ecl=np.array([self.observers[0].lamb,self.observers[0].beta]),
                #Sampling
                Np=self.planets[0].N,Nr=self.rings[0].N,Nb=100,Ns=30,
                #Physical properties
                physics=dict(
                    #Albedos
                    AS=0.5,AL=0.5,
                    #Ring geometrical opacity
                    taug=1.0, #Geometrical opacity
                    diffeff=1.0, #Diffraction efficiency
                    #Law of diffuse reflection on ring surface
                    reflection_rings_law=lambda x,y:x,
                    #Observations wavelength
                    wavelength=550e-9,
                    #Ring particle propeties (see French & Nicholson, 2000)
                    particles=dict(q=3,s0=100e-6,smin=1e-2,smax=1e2,Qsc=1,Qext=2),
                    #Stellar limb darkening
                    limb_cs=[0.6550],
                )
            )
            self.RP=RingedPlanet(**self._ringedplanet)
            return self.RP

    def _list2Objects(self,attr,kind,comps):
        if comps is None:
            exec(f"self.{attr}=[]")
        else:
            #Check if stars is a list
            try:comps[0]
            except:comps=[comps]
            exec(f"self.{attr}=[]")
            for comp in comps:
                try:
                    comp.__dict__
                    exec(f"self.{attr}+=[comp]")
                except:
                    exec(f"self.{attr}+=[{kind}(**comp)]")

System.addStar=addStar
System.addPlanet=addPlanet
System.addRing=addRing
System.addObserver=addObserver
System.__doc__=System_doc

