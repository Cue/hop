#!/usr/bin/env lua

-- Copyright 2011 The hop Authors.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

json = require("json")

function startswith(given, lookup)
  return string.sub(given, 1, string.len(lookup)) == lookup
end


function expanduser(p, i)
  if string.sub(p, 1, 1) == '~' then
    local home = os.getenv('HOME')
    return home..string.sub(p,2)
  else
    return p
  end
end


function removePrefix(str, pat)
  for i = 1, #str do
    local c = str:sub(i, i)
    if (c ~= pat)
      then
        return str:sub(i)
      end
    end
end


function backtick(cmd, raw)
  local f = assert(io.popen(cmd, 'r'))
  local s = assert(f:read('*a'))
  f:close()
  if raw then return s end
  s = string.gsub(s, '^%s+', '')
  s = string.gsub(s, '%s+$', '')
  s = string.gsub(s, '[\n\r]+', ' ')
  return s
end


Hop = {}


Hop.getAllEntries = function()
  local jsonEntries = json.decode(io.open(expanduser('~/.hop.json.db')):read('*all'))
  return jsonEntries
end


Hop.search = function(request)
  local possible = {}
  local items = Hop.getAllEntries()
  for k, v in pairs(items) do
    if (startswith(k, request))
    then
      possible[k] = v
    end
  end
  return possible

end


Hop.hop = function(request)
  local results = Hop.search(request)
  local value
  local key
  for k, p in pairs(results) do key = k; value = p break end
  if not (value)
  then
    print ('No value for ' .. request)
    return
  end
  print(key)
  print(value)
  if (startswith(value, '$server$'))
  then
    os.exit(254)
  else
    os.exit(255)
  end
end


Hop.autocomplete = function(request)
  local keys = {}
  for k in pairs(Hop.search(request)) do table.insert(keys, k) end
  print(table.concat(keys, '\n'))
end


Hop.dispatch = function(argv)
  if not (argv[1]) then return end
  if (startswith(argv[1], '-'))
  then
    local commandName = removePrefix(argv[1], '-')
    if not (Hop[commandName])
    then
      print (backtick('hop-python-script ' .. table.concat(argv, ' ')))
      return
    else
      if not (argv[2]) then return end
      return Hop[commandName](argv[2])
    end
  end

  return Hop.hop(argv[1])

end

Hop.dispatch(arg)