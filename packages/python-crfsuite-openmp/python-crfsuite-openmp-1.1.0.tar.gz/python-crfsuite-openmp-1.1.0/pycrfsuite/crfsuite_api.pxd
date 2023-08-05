from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "../crfsuite/include/crfsuite.h":
    ctypedef enum:
        CRFSUITE_SUCCESS
        CRFSUITEERR_UNKNOWN         # Unknown error occurred.
        CRFSUITEERR_OUTOFMEMORY     # Insufficient memory.
        CRFSUITEERR_NOTSUPPORTED    # Unsupported operation.
        CRFSUITEERR_INCOMPATIBLE    # Incompatible data.
        CRFSUITEERR_INTERNAL_LOGIC  # Internal error.
        CRFSUITEERR_OVERFLOW        # Overflow.
        CRFSUITEERR_NOTIMPLEMENTED  # Not implemented.


cdef extern from "../crfsuite/include/crfsuite_api.hpp" namespace "CRFSuite":
    cdef cppclass Attribute:
        string attr
        double value

        Attribute()
        Attribute(string)
        Attribute(string, double)

    cdef cppclass Pattern:
        vector[int] lines
        vector[int] columns
        Pattern()

    ctypedef vector[Pattern] Patterns
    ctypedef vector[Attribute] Item
    ctypedef vector[Item] ItemSequence
    ctypedef vector[string] StringList

    cdef string version()
    cdef Item make_patterns(Patterns, ItemSequence, int)
    cdef ItemSequence full_make_patterns(Patterns, ItemSequence)


cdef extern from "trainer_wrapper.hpp" namespace "CRFSuiteWrapper":

    ctypedef object (*messagefunc)(object self, string message)

    cdef cppclass Trainer:
        Trainer() except +
        void set_handler(object, messagefunc) except +
        void clear() except +
        void append(ItemSequence, StringList, int) except +
        void append_pattern(ItemSequence, StringList, Patterns, int) except +
        bint select(string, string) except +
        int train(string, int) except +
        StringList params() except +
        void set(string, string) except +
        string get(string) except +
        string help(string) except +
        void _init_hack() except +


cdef extern from "tagger_wrapper.hpp" namespace "CRFSuiteWrapper":

    ctypedef object (*messagefunc)(object self, string message)

    cdef cppclass Tagger:
        Tagger() except +
        int open(string) except +
        int open(const void*, size_t) except +
        void close() except +
        StringList labels() except +
        StringList tag(ItemSequence) except +
        void set(ItemSequence) except +
        void set_pattern(ItemSequence, Patterns) except +
        StringList viterbi() except +
        double probability(StringList) except +
        double marginal(string, int) except +
        void dump(int) except +
        void dump2() except +
