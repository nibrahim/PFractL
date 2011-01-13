# Copyright (C) 2002 Noufal Ibrahim <noufal@cisco.com>
#
# This program is part of PfractL
#
# PfractL is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


class Stack:
    def __init__(self):
        self.stack=[]

    def push(self,item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0 :
            print "----- Pop from empty stack ----"
            print "----- Aborting ------"
        else:
            return self.stack.pop()

    def dump(self):
        print self.stack
    
    
