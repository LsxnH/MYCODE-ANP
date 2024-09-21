// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME PhysicsAnpBaseDictReflexDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "/hepustc/home/hengli/testarea/AnpWH/source/PhysicsNtuple/PhysicsAnpBase/PhysicsAnpBase/PhysicsAnpBaseDict.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *AnpcLcLBase_Dictionary();
   static void AnpcLcLBase_TClassManip(TClass*);
   static void *new_AnpcLcLBase(void *p = 0);
   static void *newArray_AnpcLcLBase(Long_t size, void *p);
   static void delete_AnpcLcLBase(void *p);
   static void deleteArray_AnpcLcLBase(void *p);
   static void destruct_AnpcLcLBase(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::Base*)
   {
      ::Anp::Base *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::Base));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::Base", "Handle.h", 38,
                  typeid(::Anp::Base), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLBase_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::Base) );
      instance.SetNew(&new_AnpcLcLBase);
      instance.SetNewArray(&newArray_AnpcLcLBase);
      instance.SetDelete(&delete_AnpcLcLBase);
      instance.SetDeleteArray(&deleteArray_AnpcLcLBase);
      instance.SetDestructor(&destruct_AnpcLcLBase);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::Base*)
   {
      return GenerateInitInstanceLocal((::Anp::Base*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::Base*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLBase_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::Base*)0x0)->GetClass();
      AnpcLcLBase_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLBase_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLRegistry_Dictionary();
   static void AnpcLcLRegistry_TClassManip(TClass*);
   static void *new_AnpcLcLRegistry(void *p = 0);
   static void *newArray_AnpcLcLRegistry(Long_t size, void *p);
   static void delete_AnpcLcLRegistry(void *p);
   static void deleteArray_AnpcLcLRegistry(void *p);
   static void destruct_AnpcLcLRegistry(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::Registry*)
   {
      ::Anp::Registry *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::Registry));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::Registry", "Registry.h", 45,
                  typeid(::Anp::Registry), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLRegistry_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::Registry) );
      instance.SetNew(&new_AnpcLcLRegistry);
      instance.SetNewArray(&newArray_AnpcLcLRegistry);
      instance.SetDelete(&delete_AnpcLcLRegistry);
      instance.SetDeleteArray(&deleteArray_AnpcLcLRegistry);
      instance.SetDestructor(&destruct_AnpcLcLRegistry);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::Registry*)
   {
      return GenerateInitInstanceLocal((::Anp::Registry*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::Registry*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLRegistry_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::Registry*)0x0)->GetClass();
      AnpcLcLRegistry_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLRegistry_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLCallback_Dictionary();
   static void AnpcLcLCallback_TClassManip(TClass*);
   static void delete_AnpcLcLCallback(void *p);
   static void deleteArray_AnpcLcLCallback(void *p);
   static void destruct_AnpcLcLCallback(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::Callback*)
   {
      ::Anp::Callback *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::Callback));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::Callback", "AlgEvent.h", 51,
                  typeid(::Anp::Callback), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLCallback_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::Callback) );
      instance.SetDelete(&delete_AnpcLcLCallback);
      instance.SetDeleteArray(&deleteArray_AnpcLcLCallback);
      instance.SetDestructor(&destruct_AnpcLcLCallback);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::Callback*)
   {
      return GenerateInitInstanceLocal((::Anp::Callback*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::Callback*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLCallback_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::Callback*)0x0)->GetClass();
      AnpcLcLCallback_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLCallback_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLAlgEvent_Dictionary();
   static void AnpcLcLAlgEvent_TClassManip(TClass*);
   static void delete_AnpcLcLAlgEvent(void *p);
   static void deleteArray_AnpcLcLAlgEvent(void *p);
   static void destruct_AnpcLcLAlgEvent(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::AlgEvent*)
   {
      ::Anp::AlgEvent *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::AlgEvent));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::AlgEvent", "AlgEvent.h", 63,
                  typeid(::Anp::AlgEvent), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLAlgEvent_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::AlgEvent) );
      instance.SetDelete(&delete_AnpcLcLAlgEvent);
      instance.SetDeleteArray(&deleteArray_AnpcLcLAlgEvent);
      instance.SetDestructor(&destruct_AnpcLcLAlgEvent);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::AlgEvent*)
   {
      return GenerateInitInstanceLocal((::Anp::AlgEvent*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::AlgEvent*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLAlgEvent_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::AlgEvent*)0x0)->GetClass();
      AnpcLcLAlgEvent_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLAlgEvent_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLHistMan_Dictionary();
   static void AnpcLcLHistMan_TClassManip(TClass*);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::HistMan*)
   {
      ::Anp::HistMan *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::HistMan));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::HistMan", "HistMan.h", 178,
                  typeid(::Anp::HistMan), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLHistMan_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::HistMan) );
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::HistMan*)
   {
      return GenerateInitInstanceLocal((::Anp::HistMan*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::HistMan*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLHistMan_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::HistMan*)0x0)->GetClass();
      AnpcLcLHistMan_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLHistMan_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLReadNtuple_Dictionary();
   static void AnpcLcLReadNtuple_TClassManip(TClass*);
   static void *new_AnpcLcLReadNtuple(void *p = 0);
   static void *newArray_AnpcLcLReadNtuple(Long_t size, void *p);
   static void delete_AnpcLcLReadNtuple(void *p);
   static void deleteArray_AnpcLcLReadNtuple(void *p);
   static void destruct_AnpcLcLReadNtuple(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::ReadNtuple*)
   {
      ::Anp::ReadNtuple *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::ReadNtuple));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::ReadNtuple", "ReadNtuple.h", 50,
                  typeid(::Anp::ReadNtuple), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLReadNtuple_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::ReadNtuple) );
      instance.SetNew(&new_AnpcLcLReadNtuple);
      instance.SetNewArray(&newArray_AnpcLcLReadNtuple);
      instance.SetDelete(&delete_AnpcLcLReadNtuple);
      instance.SetDeleteArray(&deleteArray_AnpcLcLReadNtuple);
      instance.SetDestructor(&destruct_AnpcLcLReadNtuple);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::ReadNtuple*)
   {
      return GenerateInitInstanceLocal((::Anp::ReadNtuple*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::ReadNtuple*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLReadNtuple_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::ReadNtuple*)0x0)->GetClass();
      AnpcLcLReadNtuple_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLReadNtuple_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *AnpcLcLRunModule_Dictionary();
   static void AnpcLcLRunModule_TClassManip(TClass*);
   static void *new_AnpcLcLRunModule(void *p = 0);
   static void *newArray_AnpcLcLRunModule(Long_t size, void *p);
   static void delete_AnpcLcLRunModule(void *p);
   static void deleteArray_AnpcLcLRunModule(void *p);
   static void destruct_AnpcLcLRunModule(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Anp::RunModule*)
   {
      ::Anp::RunModule *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::Anp::RunModule));
      static ::ROOT::TGenericClassInfo 
         instance("Anp::RunModule", "RunModule.h", 50,
                  typeid(::Anp::RunModule), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AnpcLcLRunModule_Dictionary, isa_proxy, 4,
                  sizeof(::Anp::RunModule) );
      instance.SetNew(&new_AnpcLcLRunModule);
      instance.SetNewArray(&newArray_AnpcLcLRunModule);
      instance.SetDelete(&delete_AnpcLcLRunModule);
      instance.SetDeleteArray(&deleteArray_AnpcLcLRunModule);
      instance.SetDestructor(&destruct_AnpcLcLRunModule);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Anp::RunModule*)
   {
      return GenerateInitInstanceLocal((::Anp::RunModule*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Anp::RunModule*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AnpcLcLRunModule_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::Anp::RunModule*)0x0)->GetClass();
      AnpcLcLRunModule_TClassManip(theClass);
   return theClass;
   }

   static void AnpcLcLRunModule_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_AnpcLcLBase(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::Base : new ::Anp::Base;
   }
   static void *newArray_AnpcLcLBase(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::Base[nElements] : new ::Anp::Base[nElements];
   }
   // Wrapper around operator delete
   static void delete_AnpcLcLBase(void *p) {
      delete ((::Anp::Base*)p);
   }
   static void deleteArray_AnpcLcLBase(void *p) {
      delete [] ((::Anp::Base*)p);
   }
   static void destruct_AnpcLcLBase(void *p) {
      typedef ::Anp::Base current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::Base

namespace ROOT {
   // Wrappers around operator new
   static void *new_AnpcLcLRegistry(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::Registry : new ::Anp::Registry;
   }
   static void *newArray_AnpcLcLRegistry(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::Registry[nElements] : new ::Anp::Registry[nElements];
   }
   // Wrapper around operator delete
   static void delete_AnpcLcLRegistry(void *p) {
      delete ((::Anp::Registry*)p);
   }
   static void deleteArray_AnpcLcLRegistry(void *p) {
      delete [] ((::Anp::Registry*)p);
   }
   static void destruct_AnpcLcLRegistry(void *p) {
      typedef ::Anp::Registry current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::Registry

namespace ROOT {
   // Wrapper around operator delete
   static void delete_AnpcLcLCallback(void *p) {
      delete ((::Anp::Callback*)p);
   }
   static void deleteArray_AnpcLcLCallback(void *p) {
      delete [] ((::Anp::Callback*)p);
   }
   static void destruct_AnpcLcLCallback(void *p) {
      typedef ::Anp::Callback current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::Callback

namespace ROOT {
   // Wrapper around operator delete
   static void delete_AnpcLcLAlgEvent(void *p) {
      delete ((::Anp::AlgEvent*)p);
   }
   static void deleteArray_AnpcLcLAlgEvent(void *p) {
      delete [] ((::Anp::AlgEvent*)p);
   }
   static void destruct_AnpcLcLAlgEvent(void *p) {
      typedef ::Anp::AlgEvent current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::AlgEvent

namespace ROOT {
} // end of namespace ROOT for class ::Anp::HistMan

namespace ROOT {
   // Wrappers around operator new
   static void *new_AnpcLcLReadNtuple(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::ReadNtuple : new ::Anp::ReadNtuple;
   }
   static void *newArray_AnpcLcLReadNtuple(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::ReadNtuple[nElements] : new ::Anp::ReadNtuple[nElements];
   }
   // Wrapper around operator delete
   static void delete_AnpcLcLReadNtuple(void *p) {
      delete ((::Anp::ReadNtuple*)p);
   }
   static void deleteArray_AnpcLcLReadNtuple(void *p) {
      delete [] ((::Anp::ReadNtuple*)p);
   }
   static void destruct_AnpcLcLReadNtuple(void *p) {
      typedef ::Anp::ReadNtuple current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::ReadNtuple

namespace ROOT {
   // Wrappers around operator new
   static void *new_AnpcLcLRunModule(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::RunModule : new ::Anp::RunModule;
   }
   static void *newArray_AnpcLcLRunModule(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) ::Anp::RunModule[nElements] : new ::Anp::RunModule[nElements];
   }
   // Wrapper around operator delete
   static void delete_AnpcLcLRunModule(void *p) {
      delete ((::Anp::RunModule*)p);
   }
   static void deleteArray_AnpcLcLRunModule(void *p) {
      delete [] ((::Anp::RunModule*)p);
   }
   static void destruct_AnpcLcLRunModule(void *p) {
      typedef ::Anp::RunModule current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Anp::RunModule

namespace {
  void TriggerDictionaryInitialization_libPhysicsAnpBaseDict_Impl() {
    static const char* headers[] = {
0    };
    static const char* includePaths[] = {
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libPhysicsAnpBaseDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/Handle.h")))  __attribute__((annotate("$clingAutoload$PhysicsAnpBase/AlgEvent.h")))  Base;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/Registry.h")))  __attribute__((annotate("$clingAutoload$PhysicsAnpBase/AlgEvent.h")))  Registry;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/AlgEvent.h")))  Callback;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/AlgEvent.h")))  AlgEvent;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/HistMan.h")))  HistMan;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/ReadNtuple.h")))  ReadNtuple;}
namespace Anp{class __attribute__((annotate("$clingAutoload$PhysicsAnpBase/RunModule.h")))  RunModule;}
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libPhysicsAnpBaseDict dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif
#ifndef HAVE_PRETTY_FUNCTION
  #define HAVE_PRETTY_FUNCTION 1
#endif
#ifndef HAVE_64_BITS
  #define HAVE_64_BITS 1
#endif
#ifndef __IDENTIFIER_64BIT__
  #define __IDENTIFIER_64BIT__ 1
#endif
#ifndef ATLAS
  #define ATLAS 1
#endif
#ifndef GAUDI_V20_COMPAT
  #define GAUDI_V20_COMPAT 1
#endif
#ifndef ATLAS_GAUDI_V21
  #define ATLAS_GAUDI_V21 1
#endif
#ifndef HAVE_GAUDI_PLUGINSVC
  #define HAVE_GAUDI_PLUGINSVC 1
#endif
#ifndef XAOD_ANALYSIS
  #define XAOD_ANALYSIS 1
#endif
#ifndef ROOTCORE_RELEASE_SERIES
  #define ROOTCORE_RELEASE_SERIES 25
#endif
#ifndef PACKAGE_VERSION
  #define PACKAGE_VERSION "PhysicsAnpBase-v1"
#endif
#ifndef PACKAGE_VERSION_UQ
  #define PACKAGE_VERSION_UQ PhysicsAnpBase-v1
#endif
#ifndef EIGEN_DONT_VECTORIZE
  #define EIGEN_DONT_VECTORIZE 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
// -*- c++ -*-
#ifndef ANP_PHYSICSBASE_DICT_H
#define ANP_PHYSICSBASE_DICT_H

#include "PhysicsAnpBase/AlgEvent.h"
#include "PhysicsAnpBase/DataPair.h"
#include "PhysicsAnpBase/HistMan.h"
#include "PhysicsAnpBase/Registry.h"
#include "PhysicsAnpBase/ReadNtuple.h"
#include "PhysicsAnpBase/RunModule.h"
#include "PhysicsAnpBase/UtilBase.h"

#ifdef __GCCXML__

namespace Anp
{
  template void Registry::Set<int>        (const std::string &, const int &);
  template void Registry::Set<double>     (const std::string &, const double &);
  template void Registry::Set<std::string>(const std::string &, const std::string &);
  template void Registry::Set<Registry>   (const std::string &, const Registry &);
}

#endif
#endif

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"Anp::AlgEvent", payloadCode, "@",
"Anp::Base", payloadCode, "@",
"Anp::Callback", payloadCode, "@",
"Anp::GetRecursiveDir", payloadCode, "@",
"Anp::HistMan", payloadCode, "@",
"Anp::ReadNtuple", payloadCode, "@",
"Anp::Registry", payloadCode, "@",
"Anp::Round2Pair", payloadCode, "@",
"Anp::RunModule", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libPhysicsAnpBaseDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libPhysicsAnpBaseDict_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libPhysicsAnpBaseDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libPhysicsAnpBaseDict() {
  TriggerDictionaryInitialization_libPhysicsAnpBaseDict_Impl();
}
